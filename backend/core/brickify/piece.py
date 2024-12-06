from uuid import UUID 

from brickpy import Piece

from .part import BrickifyPlate
from .color import BrickifyColor

from ..database.piece import PiecePriceData, PiecePlate

class BrickifyPiece(Piece):
    """
    
    """
    def __init__(
        self,
        uuid : UUID,
        plate : BrickifyPlate,
        color : BrickifyColor,
        price : PiecePriceData
        ):
        super().__init__(plate, color)
        self.uuid = uuid
        self.price = price

 
    @classmethod
    def from_model(cls, model : PiecePlate):
        return cls(
            uuid = model.uuid,
            plate = BrickifyPlate.from_model(model.part),
            color = BrickifyColor.from_model(model.color),
            price = model.price
        )
    