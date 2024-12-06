import uuid 
import json 
import logging 

from fastapi import APIRouter, Request

from ..dependencies import get_database

from ...core.database.piecelist import get_pieces_from_criteria
from ...core.database.database import dataclass_to_dict

router = APIRouter(prefix="/piece")

@router.get("")
async def get_pieces(
    request : Request, 
    ppsUsedLessThan : float = None,
    ppsNewLessThan : float = None,
    numSetsGreaterThan : int = None,
    totalInSetsGreaterThan : int = None,
    yrsProducedGreaterThan : int = None
    ):
    """
    get the pieces that fit the given criteria

    ppsUsedLessThan : float - used price per stud is less than
    ppsNewLessThan : float - new price per stud is less than
    numSetsGreaterThan : float - number of sets with piece must be greater than
    totalInSetsGreaterThan : float - the total number of times the piece appears in all sets combined greater than
    yrsProducedGreaterThan : float = produced for more than x years 
    """
    database = get_database(request)

    pieces = await get_pieces_from_criteria(
        database = database,
        price_per_stud_used_less_than = ppsUsedLessThan, 
        price_per_stud_new_less_than = ppsNewLessThan, 
        number_of_sets_with_piece_greater_than = numSetsGreaterThan, 
        total_number_in_sets_greater_than = totalInSetsGreaterThan, 
        years_produced_greater_than = yrsProducedGreaterThan
    )
    
    return dataclass_to_dict(pieces)
