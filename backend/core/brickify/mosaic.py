from uuid import UUID
from typing import Dict

from brickpy import Mosaic
from motor.core import AgnosticDatabase

from .piece import BrickifyPiece
from .piecelist import PiecelistPieceRaw
from ..database.database import get_document
from ..database.mosaic import MosaicStandard, MosaicPieceRaw, MosaicLocation

class BrickifyMosaic(Mosaic):
    def __init__(self, size : tuple[int, int]):
        """
        Since no model exists when these are being created from scratch it can be none.
        """
        super().__init__(size)
        self.pieces : Dict[BrickifyPiece, list[tuple[bool, tuple[int, int]]]] = {} #redefining for the type hints


    @classmethod
    def from_model(cls, model : MosaicStandard):
        mosaic = cls(size = model.size)

        #add in the fits
        for piece_data in model.pieces:
            piece = BrickifyPiece.from_model(piece_data.piece)
            for fit in piece_data.fits:
                mosaic.add_piece(piece, fit.rotated, fit.location)

        return mosaic

    
    def get_piece_data(self) -> list[PiecelistPieceRaw]:
        """
        make uploading easier
        """
        piece_data = []

        for piece, fits in self.pieces.items():
            fit_objects = [MosaicLocation(rotated = fit[0], location = fit[1]) for fit in fits]
            piece_data.append(MosaicPieceRaw(
                    piece_uuid = piece.uuid,
                    fits = fit_objects
                )
            )
        return piece_data
    

async def get_brickpy_mosaic(database : AgnosticDatabase, uuid : UUID) -> BrickifyMosaic:
    """
    throws no model exist if no documents are returned
    """
    mosaic_model = await get_document(
        model = MosaicStandard,
        database = database,
        match_query={"$match" : {"uuid" : uuid}}
    )
    return BrickifyMosaic.from_model(mosaic_model)


