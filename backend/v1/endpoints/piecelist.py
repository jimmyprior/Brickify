import uuid 
import json 
import logging 

import typing 


from fastapi import APIRouter, Request, HTTPException, Query
from motor.core import AgnosticDatabase #just used for type hinting

from ..body.piecelist import CriteriaModel, CreateModel
from ..dependencies import get_database

from ...core.database.piecelist import get_pieces_from_criteria, upload_piecelist, PiecelistStandard
from ...core.database.database import dataclass_to_dict, get_document, ModelDoesNotExist

router = APIRouter(prefix="/piecelist")


#UNTESTED

@router.post("")
async def create_piecelist(request : Request, data : CreateModel):
    """
    create piecelist and return uuid
    """
    database = get_database(request)

    _uuid = await upload_piecelist(
        database = database,
        name = data.name,
        pieces = data.pieces,
        description=data.description
    )

    return {
        "uuid" : _uuid
    }


@router.get("")
async def get_piecelists(
    request : Request, 
    ids : typing.Annotated[list[uuid.UUID], Query()],
    colors : bool = False,
    ) -> list[dict]:
    """
        "name" : data.name,
        "description" : data.description,
        "colors" : [
            "lab" : cielab,
            "rgb" : rgb,
            "maxArea" : max_area (max area allowed by qty)
        ] <- optional
    """
    database = get_database(request)

    async def _get_piecelist(_uuid : uuid.UUID):
        """
            "name" : data.name,
            "description" : data.description,
            "colors" : [
                "lab" : cielab,
                "rgb" : rgb,
                "maxArea" : max_area (max area allowed by qty)
            ]
        """

        try:
            data = await get_document(
                model=PiecelistStandard,
                database=database, 
                pipeline=[{"$match" : {"uuid" : _uuid}}]
            )
        except ModelDoesNotExist as e: 
            msg = f"Piecelist {_uuid} does not exist"
            logging.warn(msg)
            #404 status
            raise HTTPException(
                status_code=404,
                detail=msg
            )
        
        return_data = {
            "id" : _uuid,
            "name" : data.name,
            "description" : data.description,
            "colors" : []
        }
        
        if colors: # if colors is true, get the color info

            for piecelist_piece in data.pieces:
                qty = piecelist_piece.qty 
                cielab = piecelist_piece.piece.color.spaces.cielab
                rgb = piecelist_piece.piece.color.spaces.rgb
                size = piecelist_piece.piece.part.size     
                if qty < 0:
                    max_area = -1
                else:
                    max_area = size[0] * size[1] * qty

                return_data["colors"].append({
                    "lab" : cielab,
                    "rgb" : rgb,
                    "maxArea" : max_area
                })
        
        if (not colors):
            return_data.pop("colors")

        return return_data

    piecelists = []

    for _uuid in ids:
        piecelist = await _get_piecelist(_uuid)
        piecelists.append(piecelist)        

    return piecelists