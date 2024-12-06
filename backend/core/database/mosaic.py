from uuid import UUID
from typing import Optional

from pydantic import dataclasses
from motor.core import AgnosticDatabase


from .piece import PIECE_LOOKUP, PiecePlate
from .database import upload_document

COLLECTION_NAME = "mosaics"


@dataclasses.dataclass
class MosaicLocation:
    rotated : bool
    location : tuple[int, int]

@dataclasses.dataclass
class MosaicPieceRaw:
    piece_uuid : UUID
    fits : list[MosaicLocation] 


@dataclasses.dataclass
class MosaicTime:
    initialized : int
    completed : int


@dataclasses.dataclass
class MosaicPiece:
    """
    piece : piece data 
    fits : list of locations and orientations on the mosaic
    """
    piece : PiecePlate
    fits : list[MosaicLocation]


@dataclasses.dataclass
class MosaicRaw:
    """
    optional because they are not guranteed for uninitialized mosaics
    """
    uuid : UUID
    created : int
    piecelist_uuid : Optional[UUID] = None
    owner_uuid : Optional[UUID] = None
    size : Optional[tuple[int, int]] = None
    pieces : Optional[list[MosaicPieceRaw]] = None
    time : Optional[MosaicTime] = None

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME


@dataclasses.dataclass
class MosaicStandard:
    """
    optional because they are not guranteed for uninitialized mosaics
    """
    uuid : UUID
    pieces : Optional[list[MosaicPiece]]
    piecelist_uuid : Optional[UUID] = None
    owner_uuid : Optional[UUID] = None
    size : Optional[tuple[int, int]] = None

    AGGREGATE = [
        {
            "$unwind" : "$pieces" #https://stackoverflow.com/questions/13895006/unwind-empty-array (empty piece arrays will result in no mosaic being returned)
        },
        *PIECE_LOOKUP,
        {
            "$group" : {
                "_id" : {
                    "_id" : "$_id" #regroup them by _id
                },
                "pieces": { 
                    "$push" : {
                        "piece" : {"$first": "$piece_data"}, 
                        "fits" : "$pieces.fits"
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


@dataclasses.dataclass
class MosaicPriceEstimate:
    used : float
    new : float


@dataclasses.dataclass
class MosaicStandardPrice:
    uuid : UUID 
    price : MosaicPriceEstimate
    piecelist_uuid : Optional[UUID] = None
    owner_uuid : Optional[UUID] = None
    size : Optional[tuple[int, int]] = None
    time : Optional[MosaicTime] = None

    #requires previous stage to have pieces loaded in with fits data as shown above
    #multiple number of fits times the price of the piece
    AGGREGATE = [
        *MosaicStandard.AGGREGATE,
        {
            "$addFields": {
                f"price.{condtion}" : {
                    "$sum": {
                        "$map": {
                            "input": "$pieces", 
                            "in": {
                                "$multiply": [
                                    {"$size": "$$this.fits"}, 
                                    f"$$this.piece.price.{condtion}.avg"
                                ]
                            }
                        }
                    }
                } for condtion in ("new", "used")
            }
        }
    ]
    COLLECTION = COLLECTION_NAME


async def upload_mosaic_document(
    database : AgnosticDatabase,
    piecelist_uuid : UUID = None,
    owner_uuid : UUID = None,
    size : tuple[int, int] = None,
    pieces : list[MosaicPieceRaw] = None,
    time : MosaicTime = None    
    ):
    """
    """
    return await upload_document(
        document = {
            "piecelist_uuid" : piecelist_uuid,
            "owner_uuid" : owner_uuid,
            "size" : size,
            "pieces" : pieces,
            "time" : time
        }, 
        collection = database[COLLECTION_NAME]
    )

