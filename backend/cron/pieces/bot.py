import os
import json
import logging
import asyncio 
import uuid 

from .api import Rebrickable
from .helpers import get_color_data, get_piece_data, get_plate_data

from ...core.database.collections.color import upload_color_document, ColorSpaces, ExternalIDs, ExternalNames
from ...core.database.collections.part import upload_part_document
from ...core.database.collections.piece import upload_piece_document, Production, PieceUsage

async def get_data_from_rebrickable(api_key : str) -> dict:
    """
    gets data from every plate from rebrickable 
        stores plate data in mongodb parts collection 
    gets data from every color from rebrickable 
        stores color data in mongodb colors collection 
    gets data for every part and color combo from rebrickable
        stores data in pieces collection where color_uuid and part_uuid 
        correspond to the respective plate and color uuid's returned 
        when inserting into mongodb
    """
    api = Rebrickable(api_key=api_key)

    color_dict = {} #{"uuid" : {...data}, ...}
    async for color_data in get_color_data(api):
        #insert to database and add to color_dict
        color_uuid = await upload_color_document(
            name=color_data["name"],
            transparent=color_data["transparent"],
            spaces=ColorSpaces(**color_data["spaces"]),
            ids=ExternalIDs(**color_data["ids"]),
            names=ExternalNames(**color_data["names"])
        )
        color_dict[str(color_uuid)] = color_data
        logging.info(f"Added color {color_uuid} to MongoDB")

    plate_dict = {} #{"uuid" : {...data}, ...}
    async for plate_data in get_plate_data(api):
        #insert to database and add to plate_dict
        plate_uuid = await upload_part_document(
            name = plate_data["name"],
            group = plate_data["group"],
            ids = ExternalIDs(**plate_data["ids"]),
            size = plate_data["size"]
        )
        plate_dict[str(plate_uuid)] = plate_data 
        logging.info(f"Added plate {plate_uuid} to MongoDB")

    piece_dict = {} #{"uuid" : {...data}, ...}
    #uuids are stored as strings here so that they can be dumped as json but make sure 
    #to treat them as actual uuids when writing to the database
    async for piece_data in get_piece_data(api, color_dict, plate_dict):
        #insert to database and add to piece_dict
        piece_uuid = await upload_piece_document(
            part_uuid=uuid.UUID(piece_data["part_uuid"]),
            color_uuid=uuid.UUID(piece_data["color_uuid"]),
            production=Production(**piece_data["production"]),
            usage=PieceUsage(**piece_data["usage"]),
            pricing=[]
        )
        piece_dict[str(piece_uuid)] = piece_data
        logging.info(f"Added piece {piece_uuid} to MongoDB")
        await asyncio.sleep(2) #sleep for a bit to prevent hitting rate limit / spam

    await api.close()

    return {
        "parts" : plate_dict,
        "colors" : color_dict,
        "pieces" : piece_dict
    }

async def main(filename : str = None):

    logging.basicConfig(
        filename=f'{filename}.log', 
        encoding='utf-8', 
        level=logging.INFO, 
        format='[%(asctime)s] %(levelname)s:%(message)s'
    )

    data = await get_data_from_rebrickable(os.getenv("REBRICKABLE_API_KEY"))

    with open(f"{filename}.json", "w+") as outfile:
        outfile.write(json.dumps(data, indent=2, default=str))
    