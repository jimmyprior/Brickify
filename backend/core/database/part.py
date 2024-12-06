from enum import Enum
from uuid import UUID
from typing import Optional

from pydantic import dataclasses
from motor.core import AgnosticDatabase

from .database import upload_document

COLLECTION_NAME = "parts"

PART_LOOKUP = [
    {
        "$lookup" : {
            "from" : "parts",
            "localField" : "part_uuid",
            "foreignField" : "uuid",
            "as" : "parts",
        }
    },
    {
        "$set": {
            "part": {
                "$arrayElemAt": [
                    "$parts",
                    0
                ]
            }
        }
    }
]

@dataclasses.dataclass
class ExternalNames:
    lego : str | None
    rebrickable : str
    bricklink : str
    brickowl : str


@dataclasses.dataclass
class ExternalIDs:
    lego : str | None
    rebrickable : str
    bricklink : str
    brickowl : str


class PartType(str, Enum):
    PLATE = "PLATE"
    BASE_PLATE = "BASE_PLATE" #techinically a plate but so that it does not end up in piece lists
    PIN = "PIN"


@dataclasses.dataclass
class PartRaw:
    name : str
    uuid : UUID 
    group : PartType
    ids : ExternalIDs
    created : int
    size : Optional[tuple[int, int]] = None

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME

@dataclasses.dataclass
class PartStandard:
    name : str
    uuid : UUID 
    ids : ExternalIDs

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME


@dataclasses.dataclass
class PartPlate:
    """
    part that is for a plate
    includes special field size 
    """
    name : str
    uuid : UUID 
    ids : ExternalIDs
    size : tuple[int, int]

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME


async def upload_part_document(
    database : AgnosticDatabase,
	name : str, 
    group : PartType,
    ids : ExternalIDs,
    size : tuple[int, int]
	):
    return await upload_document(
        document = {
            "name" : name, 
            "group" : group,
            "ids" : ids,
            "size" : size
        }, 
        collection = database[COLLECTION_NAME]
    )
