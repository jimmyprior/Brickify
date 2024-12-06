import uuid 

from pydantic import BaseModel, conint

from .image import ImageModel

#https://docs.pydantic.dev/usage/types/#constrained-types


class SettingsModel(BaseModel):
    shuffle : bool = False
    maxDist : conint(ge=0, le=10000) = 10


class CreateModel(BaseModel):
    """
    {
        "image" : "base64 string",
        "pieceListID" : "uuid",
        "settings" : {
            "maxDist" : 10,
            "shuffle" : False
        }
    }
    """
    image : ImageModel
    pieceListID : uuid.UUID
    settings : SettingsModel