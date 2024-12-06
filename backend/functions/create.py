import os
import time 
import json 
import logging 
import uuid
import io

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase

from brickpy import create_mosaic_piece_optimized

from ..v1.body.mosaic import CreateModel #move this or something so that when packaging i do not have to include v1

from ..core.brickify.mosaic import BrickifyMosaic
from ..core.brickify.piecelist import get_brickpy_piecelist
from ..core.database.mosaic import upload_mosaic_document, MosaicTime
from ..core.database.database import ModelDoesNotExist

from ..core.aws.s3 import upload_file

def get_database() -> AgnosticDatabase:
    connection = AsyncIOMotorClient(
        os.getenv("DATABASE_URI"), 
        connect=False, #only connect on first query
        uuidRepresentation="standard" #uuid representation
    )
    return connection.brickify #this is the database


def upload_to_s3(mosaic_id : uuid.UUID, mosaic : BrickifyMosaic):
    """
    upload instructions and render to s3
    """
    #upload image
    render = io.BytesIO()
    mosaic.get_image().save(render, "png")

    upload_file(
        render,
        f"{mosaic_id}/render.png",
        content_type = "image/png"
    )

    instructions = io.BytesIO()
    mosaic.save_pdf_instructions(instructions)

    upload_file(
        instructions,
        f"{mosaic_id}/instructions.pdf",
        content_type = "application/pdf"
    )





async def _create_mosaic(event, context) -> dict:
    """
    lambda function that runs on aws. 
    actually creates the mosaic and uploads it to the database
    returns mosaic uuid
    """
    #get the body of the payload and convert it to a dict
    database = get_database()
    payload = json.loads(event["body"])
    #parse it using CreateModel to get expected and consistent types
    create_data = CreateModel.parse_obj(payload)
    image = create_data.image #get the PIL.Image.Image
    piecelist_uuid = create_data.pieceListID #get the piecelist uuid
    try:
        #get the actual piecelist obj 
        piecelist = await get_brickpy_piecelist(
            database=database, 
            uuid=piecelist_uuid
        )
    except ModelDoesNotExist as e:
        #if the piecelist does not exist return error 
        msg = f"Piecelist {str(piecelist_uuid)} does not exist when lambda attempted to resolve"
        logging.warning(msg)
        return {
            "statusCode" : 404,
            "error": {"msg" : msg}
        }
    
    initialized = int(time.time()) #record time when mosaic creation begins

    #actually create the mosaic
    brickify_mosaic : BrickifyMosaic = create_mosaic_piece_optimized(
        image=image, 
        piecelist=piecelist,
        shuffle=create_data.settings.shuffle,
        max_euclidean_distance=create_data.settings.maxDist,
        mosaic=BrickifyMosaic(image.size)
    )

    
    completed = int(time.time()) #record time when mosaic creation finished

    #upload mosaic to the database. returns uuid
    mosaic_uuid = await upload_mosaic_document(
        database = database,
        piecelist_uuid = piecelist_uuid,
        owner_uuid = None,
        size = brickify_mosaic.size,
        pieces = brickify_mosaic.get_piece_data(),
        time = MosaicTime(initialized=initialized, completed=completed)
    )

    upload_to_s3(mosaic_uuid, brickify_mosaic)

    logging.info(f"Created mosaic {mosaic_uuid}. Time elapsed {completed - initialized}")

    #download instructions and render to s3
    

    #return mosaic id 
    return {
        "statusCode" : 200,
        "body": {"uuid" : mosaic_uuid}
    }
