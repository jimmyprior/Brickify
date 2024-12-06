import uuid 
import json 
import logging 

from fastapi import APIRouter, Request, HTTPException
from motor.core import AgnosticDatabase #just used for type hinting

from ..body.mosaic import CreateModel
from ..dependencies import get_aiohttp_session, get_database

from ...functions.create import _create_mosaic #lambda function (if not running lambda use local)
from ...core.database.piecelist import PiecelistExist
from ...core.database.database import get_document, ModelDoesNotExist
from ...core.database.mosaic import MosaicStandardPrice
from ...core.database.database import get_document

from ...core.aws.s3 import generate_presigned_url

router = APIRouter(prefix="/mosaic")

#https://github.com/laurentS/slowapi?tab=readme-ov-file

@router.get("/{mosaic_uuid}")
async def _get_mosaic(mosaic_uuid : uuid.UUID, request : Request) -> dict:
    """
    gets the mosaic standard with price data and presigned urls for mosaic media 
    and returns dictionary with the data
    """
    database = get_database(request)

    mosaic_data : MosaicStandardPrice = await get_document(
        model = MosaicStandardPrice, 
        database = database,
        pipeline = [{"$match" : {"uuid" : mosaic_uuid}}]
    )

    #if full get instructions url and owner
    #generate presigned urls
    #maybe add bricklink xml here if full version?

    return {
        "id" : mosaic_data.uuid, 
        "time" : mosaic_data.time,
        "price" : mosaic_data.price,
        "media" : {
            "render" : generate_presigned_url(f"{mosaic_data.uuid}/render.png"),
            "instructions" : generate_presigned_url(f"{mosaic_data.uuid}/instructions.pdf")
        },
        "owner" : {"id" : mosaic_data.owner_uuid}
    }

@router.post("", response_model=None)
async def create_mosaic(
    request : Request,
    create_data : CreateModel
    ):

    database = get_database(request)
    aiohttp_session = get_aiohttp_session(request)
    """
    
    return class mosaic body. same as get_mosaic
    """
    #MAKE SURE PIECELIST EXISTS HERE
    piecelist_uuid = create_data.pieceListID
    try:
        await get_document(
            model=PiecelistExist,
            database=database, 
            pipeline=[{"$match" : {"uuid" : piecelist_uuid}}]
        )
    except ModelDoesNotExist as e: 
        msg = f"Piecelist {piecelist_uuid} does not exist"
        logging.warn(msg)
        #404 status
        raise HTTPException(
            status_code=404,
            detail=msg
        )
    
    #if not using aws local
    if False:
        #async http request so that application does not block
        #aiohttp client session should be part of the app just like the database connection
        #aiohttp_session 
        mosaic_uuid = None
        
    else:
        #if no aws function do manual
        #have to get json because dict will not convert uuids to strings
        req_data = json.loads(create_data.json(exclude={"image"}))
        req_data["image"] = create_data.image.base64 #should have this prop because created with base64

        _mosaic_data = await _create_mosaic(
            event = {"body" : json.dumps(req_data)},
            context = None
        )
        mosaic_uuid = _mosaic_data["body"]["uuid"]         
    try: 
        return await _get_mosaic(mosaic_uuid = mosaic_uuid, request=request)
    except ModelDoesNotExist:
        msg = "Failed to create mosaic"
        logging.warn(msg)
        raise HTTPException(
            status_code = 500,
            detail = msg
        )
    
    
# @router.get("/{mosaic_id}")
async def get_mosaic(request : Request, mosaic_id : uuid.UUID):
    """
    GET mosaic data
    """
    database = get_database(request)
    #return mosaic (full or preview), 404 (not found) or 403 (acess denied)
    return {}
    # try: 
    #     return await _get_mosaic(mosaic_uuid = mosaic_id)
    # except ModelDoesNotExist:
    #     return {
    #         "error" : "mosaic with that id does not exist"
    #     }

#could use a depends to just quick get the mosaic maybe? 
# @router.get("/{mosaic_id}/bricklink")
async def get_bricklink(request : Request, mosaic_id : uuid.UUID):
    """
    get the bricklink xml 
    """
    database = get_database(request)
    #cahce on cloudflare
    return {}