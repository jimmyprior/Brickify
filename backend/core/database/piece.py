import uuid
import typing

from pydantic import dataclasses
from motor.core import AgnosticDatabase

from .color import ColorStandard, COLOR_LOOKUP
from .part import PartStandard, PartPlate, PART_LOOKUP
from .database import upload_document


COLLECTION_NAME = "pieces"

PRICE_QUERY = [
        {
        "$set": {
            "pricing": {
                "$sortArray": {
                    "input": "$pricing",
                    "sortBy": {
                        "scraped": -1
                    }
                }
            }
        }
    },
    {
        "$set": {
            "price": {
                "$arrayElemAt": [
                    "$pricing",
                    0
                ]
            }
        }
    } 
]

PIECE_QUERY = [*PART_LOOKUP, *COLOR_LOOKUP, *PRICE_QUERY]

PIECE_LOOKUP = [
    {
        "$lookup" : {
            "from" : "pieces",
            "localField" : "pieces.piece_uuid",
            "foreignField" : "uuid",
            "as" : "piece_data",
            "pipeline" : PIECE_QUERY
        }
    }
]

#search for pieces that fit criteria

@dataclasses.dataclass
class PriceData:
    """
    """
    min: float
    max: float
    avg: float
    pps: float


@dataclasses.dataclass
class PiecePriceData:
    """
    """
    new : PriceData
    used : PriceData
    scraped : int


@dataclasses.dataclass
class Production:
    start : int 
    end : int | bool


@dataclasses.dataclass
class PieceUsage:
    """
    num_sets : number of sets the piece occured in
    num_in_sets : sum of the number of occurances in each set it has occured in 
    """
    num_sets : int
    num_in_sets : int


@dataclasses.dataclass
class PieceRaw:
    """
    uuid : piece id
    part_uuid : id of the part 
    color_uuid : id of the color 
    """
    uuid : uuid.UUID
    part_uuid : uuid.UUID
    color_uuid : uuid.UUID
    production : Production
    pricing : list[PiecePriceData]
    usage : PieceUsage
    created : int

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME


@dataclasses.dataclass
class PieceBase:
    """
    NOT TO BE CONFUSED WITH PLATE
    """
    uuid : uuid.UUID
    production : Production
    part : PartStandard
    color : ColorStandard
    price : typing.Optional[PiecePriceData] = None

    AGGREGATE = PIECE_QUERY
    COLLECTION = COLLECTION_NAME


@dataclasses.dataclass
class PiecePlate(PieceBase):
    """
    
    """
    uuid : uuid.UUID
    production : Production
    part : PartPlate
    color : ColorStandard
    price : typing.Optional[PiecePriceData] = None

    AGGREGATE = PIECE_QUERY
    COLLECTION = COLLECTION_NAME


async def upload_piece_document(
    database : AgnosticDatabase,
    part_uuid : uuid.UUID,
    color_uuid : uuid.UUID,
    production : Production,
    usage : PieceUsage,
    pricing : list[PiecePriceData] = []
    ) -> uuid.UUID:
    """
    """
    return await upload_document(
        document = {
            "part_uuid" : part_uuid,
            "color_uuid" : color_uuid,
            "production" : production,
            "usage" : usage,
            "pricing" : pricing
        }, 
        collection = database[COLLECTION_NAME]
    )
