from ...core.database.collections.color import upload_color_document, ColorSpaces, ExternalIDs, ExternalNames
from ...core.database.collections.part import upload_part_document
from ...core.database.collections.piece import upload_piece_document, Production, PieceUsage
import json


async def upload_data(data : dict):
    """
    data format: 

    {
        "parts" : {hash : {...}}
        "colors" : {hash : {...}
        }
        "pieces" : {
            hash : {
                color_id : #color_hash
                part_id : #part_hash
            }
        }
    }
    """ 

    for color_hash in list(data["colors"].keys()):
        
        color_data = data["colors"][color_hash]

        color_uuid = await upload_color_document(
            name=color_data["name"],
            transparent=color_data["transparent"],
            spaces=ColorSpaces(**color_data["spaces"]),
            ids=ExternalIDs(**color_data["ids"]),
            names=ExternalNames(**color_data["names"])
        )

        data["colors"][color_hash]["uuid"] = color_uuid


    for part_hash in list(data["parts"].keys()):

        part_data = data["parts"][part_hash]

        part_uuid = await upload_part_document(
            name = part_data["name"],
            group = part_data["group"],
            ids = ExternalIDs(**part_data["ids"]),
            size = part_data["size"]
        )

        data["parts"][part_hash]["uuid"] = part_uuid


    for piece_hash in data["pieces"].keys():
        """
        "-6049538917235726166": {
            "color_hash": 2615932599109005068,
            "part_hash": 5735482900421320921,
            "usage": {
                "num_sets": 8,
                "num_in_sets": 16
            },
            "production": {
                "start": 2021,
                "end": 2023
            }
        }
        """
        piece_data = data["pieces"][piece_hash]
        
        part_hash = piece_data["part_hash"]
        color_hash = piece_data["color_hash"]

        piece_uuid = await upload_piece_document(
            part_uuid=data["parts"][part_hash]["uuid"],
            color_uuid=data["colors"][color_hash]["uuid"],
            production=Production(**piece_data["production"]),
            usage=PieceUsage(**piece_data["usage"]),
            pricing=[]
        )

        data["pieces"][piece_hash]["uuid"] = piece_uuid


    with open("outfile.json", "w+") as outfile:
        outfile.write(json.dumps(data, indent=2))
