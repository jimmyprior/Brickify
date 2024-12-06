from uuid import UUID 
from typing import Self, Dict

from motor.core import AgnosticDatabase

from brickpy import PieceList

from .piece import BrickifyPiece
from ..database.database import get_document
from ..database.piecelist import PiecelistStandard, PiecelistPieceRaw, get_pieces_from_criteria


class BrickifyPiecelist(PieceList):
    def __init__(self, model : PiecelistStandard | None = None):
        super().__init__()
        self.model = model
        self.quantities : Dict[BrickifyPiece, int] = {}#for type hint


    @classmethod
    def from_model(cls : Self, model : PiecelistStandard) -> Self:
        piecelist = cls(model)
        
        for piecelist_piece_data in model.pieces:
            piecelist.add_piece(
                piece=BrickifyPiece.from_model(piecelist_piece_data.piece),
                quantity=piecelist_piece_data.qty
            )

        return piecelist
    

    def get_piece_data(self) -> list[PiecelistPieceRaw]:
        """
        formats pieces field to make uploading easier.
        """
        pieces = []
        for piece, qty in self.quantities.items():
            pieces.append(
                PiecelistPieceRaw(
                    piece_uuid = piece.uuid,
                    qty = qty
                )
            )
        return pieces
    

async def get_brickpy_piecelist(database : AgnosticDatabase, uuid : UUID) -> BrickifyPiecelist:
    """
    throws no model exist if no documents are returned
    """
    piecelist_model = await get_document(
        model = PiecelistStandard,
        database = database,
        pipeline=[{"$match" : {"uuid" : uuid}}]
    )
    return BrickifyPiecelist.from_model(piecelist_model)


async def get_brickpy_piecelist_from_criteria(
    database : AgnosticDatabase,
    price_per_stud_used_less_than : float = None,
    price_per_stud_new_less_than : float = None,
    number_of_sets_with_piece_greater_than : float = None,
    total_number_in_sets_greater_than: float = None,
    years_produced_greater_than: float = None,
    ) -> BrickifyPiecelist:
    """
    get the pieces that fit the given criteria

    price_per_stud_used_less_than : float - used price per stud is less than 
    price_per_stud_new_less_than : float - new price per stud is less than
    number_of_sets_with_piece_greater_than : float - number of sets with piece must be greater than
    total_number_in_sets_greater_than: float = the total number of times the piece appears in all sets combined greater than
    years_produced_greater_than: float = produced for more than x years 
    still_produced: bool = whether or not the piece is still produced

    returns full brickpy piecelist 
    """
    kwargs = locals()
    pieces = await get_pieces_from_criteria(**kwargs)

    piecelist = BrickifyPiecelist()
    async for piece in pieces:
        piecelist.add_piece(
            piece=piece, 
            quantity=-1
        )
    
    return piecelist