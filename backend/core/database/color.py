# import dataclasses
from uuid import UUID

from pydantic import dataclasses
from motor.core import AgnosticDatabase

from .part import ExternalIDs, ExternalNames
from .database import upload_document

#for piece query. expects object entering pipeline 
#to have color_uuid field and finds corresponding color in color collection
#because lookup returns a list only returns first result 
#if does not exist, [x] happens

COLLECTION_NAME = "colors"

COLOR_LOOKUP = [
    {
        "$lookup" : {
            "from" : "colors",
            "localField" : "color_uuid",
            "foreignField" : "uuid",
            "as" : "colors",
        }
    },
    {
        "$set": {
            "color": {
                "$arrayElemAt": [
                    "$colors",
                    0
                ]
            }
        }
    }
]

@dataclasses.dataclass
class ColorSpaces:
    """
    rgb used for drawing the pieces with Pillow 
    cielab used for comparisons
    """
    rgb : tuple[int, int, int]
    cielab : tuple[float, float, float]

@dataclasses.dataclass
class ColorRaw:
    """
    raw unmodified color data in the db
    """
    name : str
    transparent : bool
    spaces : ColorSpaces
    ids : ExternalIDs
    names : ExternalNames
    created : int

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME

@dataclasses.dataclass
class ColorStandard:
    """
    The standard color representation used by mosaic etc..
    """
    uuid : UUID
    name : str 
    spaces : ColorSpaces
    ids : ExternalIDs

    AGGREGATE = []
    COLLECTION = COLLECTION_NAME
    

async def upload_color_document(
    database : AgnosticDatabase,
    name : str,
    transparent : bool,
    spaces : ColorSpaces,
    ids : ExternalIDs,
    names : ExternalNames
    ) -> UUID:
    """
    uploads a color to the database
    """
    return await upload_document(
        document = {
            "name" : name,
            "transparent" : transparent,
            "spaces" : spaces,
            "ids" : ids,
            "names" : names
        }, 
        collection = database[COLLECTION_NAME]
    )


