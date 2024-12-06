from uuid import UUID

from pydantic import dataclasses
from motor.core import AgnosticDatabase

from .part import PART_LOOKUP
from .color import COLOR_LOOKUP
from .database import upload_document, get_projection
from .piece import PiecePlate, PIECE_LOOKUP, PRICE_QUERY

COLLECTION_NAME = "piecelists"
 
@dataclasses.dataclass
class PiecelistPieceRaw:
    piece_uuid : UUID
    qty : int

@dataclasses.dataclass
class PiecelistRaw:
    uuid : UUID
    name : str
    pieces : list[PiecelistPieceRaw]
    description : str
    updated : int
    created : int

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME

@dataclasses.dataclass
class PiecelistPiece:
    piece : PiecePlate
    qty : int
    

@dataclasses.dataclass
class PiecelistStandard:
    uuid : UUID
    name : str
    pieces : list[PiecelistPiece]
    description : str
    created : int
    updated : int = None

    AGGREGATE = [
        {
            "$unwind" : "$pieces" #https://stackoverflow.com/questions/13895006/unwind-empty-array (empty piece arrays will result in no mosaic being returned)
        },
        
        *PIECE_LOOKUP, #piece query
        {
            "$group" : {
                "_id" : {
                    "_id" : "$_id" #regroup them by _id
                },
                "pieces": { 
                    "$push" : {
                        "piece" : {"$first": "$piece_data"}, 
                        "qty" : "$pieces.qty",
                        "added" : "$pieces.added"
                    }
                },
                "doc" : { "$first": "$$ROOT" } #store data for the merged docs as data field.
            }
        },
        {
            "$replaceRoot" : {
                "newRoot": {
                    "$mergeObjects": [
                        "$doc", {
                            "pieces": "$pieces" 
                        }
                    ]
                }
            }
        },
        {
            "$project" : { #get rid of these extra fields
                "doc" : False, 
                "piece_data" : False
            }
        }
    ]
    COLLECTION = COLLECTION_NAME

async def upload_piecelist(
    database : AgnosticDatabase,
    name : str, 
    pieces : list[PiecelistPieceRaw],
    description : str
    ) -> UUID:

    return await upload_document(
        document = {
            "name" : name,
            "pieces" : pieces,
            "description" : description
        }, 
        collection = database[COLLECTION_NAME]
    )


@dataclasses.dataclass
class PiecelistExist:
    uuid : UUID
    AGGREGATE = []
    COLLECTION = COLLECTION_NAME

async def get_pieces_from_criteria(
    database : AgnosticDatabase,
    price_per_stud_used_less_than : float = None,
    price_per_stud_new_less_than : float = None,
    number_of_sets_with_piece_greater_than : float = None,
    total_number_in_sets_greater_than: float = None,
    years_produced_greater_than: float = None,
    ) -> list[PiecePlate]:
    """
    get the pieces that fit the given criteria

    price_per_stud_used_less_than : float - used price per stud is less than 
    price_per_stud_new_less_than : float - new price per stud is less than
    number_of_sets_with_piece_greater_than : float - number of sets with piece must be greater than
    total_number_in_sets_greater_than: float = the total number of times the piece appears in all sets combined greater than
    years_produced_greater_than: float = produced for more than x years 
    still_produced: bool = whether or not the piece is still produced

    returns list of piece plates 
    """

    pipeline = []

    search_conditions = []

    pipeline.append({
        "$match": {
            "$expr": {
                "$and": search_conditions
                }
            }
        }
    )

    if not (number_of_sets_with_piece_greater_than is None):
        search_conditions.append({
            "$gte": [
            "$usage.num_sets",
                number_of_sets_with_piece_greater_than
            ] 
        })

    if not (total_number_in_sets_greater_than is None):
        search_conditions.append({
            "$gte": [
            "$usage.num_in_sets",
                total_number_in_sets_greater_than
            ] 
        })

    if not (years_produced_greater_than is None):
        search_conditions.append({
            "$gte": [
                {
                    "$subtract": [
                        "$production.end",
                        "$production.start"
                    ]
                },
                years_produced_greater_than
            ]
        })
        

    pipeline.extend(PRICE_QUERY) #get the prices for all the pieces

    if not ((price_per_stud_used_less_than is None) and (price_per_stud_new_less_than is None)): 
        #if price is a filter, add price field to the documents
        #price field is the most recent price query. 
        #also filter out pieces with no price.

        search_conditions.append({
                "$gt": [
                    {
                        "$size": "$pricing"
                    },
                    0
                ]
            }
        )

        price_match = []

        pipeline.append({
            "$match": {
                "$expr": {
                    "$and": price_match
                }
            }
        })

        if price_per_stud_new_less_than:
            price_match.append({
                "$lte": [
                    "$price.new.pps",
                    price_per_stud_new_less_than
                ] 
            })

        if price_per_stud_used_less_than:
            price_match.append({
                "$lte": [
                    "$price.used.pps",
                    price_per_stud_used_less_than
                ] 
            })    

    
    pipeline.extend(PART_LOOKUP)
    pipeline.extend(COLOR_LOOKUP)
    #price already there

    #dont use normal because don't want to redo the lookups multiple times
    pipeline.append(get_projection(PiecePlate))
    
    collection = database[PiecePlate.COLLECTION]

    models = []
    async for doc in collection.aggregate(pipeline):
        models.append(PiecePlate(**doc))
    
    return models