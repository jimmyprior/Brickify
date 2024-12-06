import uuid 

from pydantic.v1 import BaseModel, conint, constr


class CriteriaModel(BaseModel):
    """
    {
        ppsUsedLessThan : float - used price per stud is less than
        ppsNewLessThan : float - new price per stud is less than
        numSetsGreaterThan : float - number of sets with piece must be greater than
        totalInSetsGreaterThan : float - the total number of times the piece appears in all sets combined greater than
        yrsProducedGreaterThan : float = produced for more than x years 
    }
    """
    ppsUsedLessThan : int
    ppsNewLessThan : int
    numSetsGreaterThan : int
    totalInSetsGreaterThan : int
    yrsProducedGreaterThan : int


from ...core.database.piecelist import PiecelistPieceRaw


class CreateModel(BaseModel):
    pieces : list[PiecelistPieceRaw]
    name : constr(min_length = 1, max_length = 50)
    description : constr(min_length = 1, max_length = 250)
