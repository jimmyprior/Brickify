from uuid import UUID
from typing import Self

from brickpy import Plate

from ..database.part import ExternalIDs, PartPlate


class BrickifyPlate(Plate):
    def __init__(
        self, 
        uuid : UUID,
        size : tuple[int, int], 
        name : str,
        external_ids : ExternalIDs,
        model : PartPlate
        ):
        super().__init__(size=size, name=name)
        self.uuid = uuid
        self.external_ids = external_ids
        self.model = model
    

    @classmethod
    def from_model(cls : Self, model : PartPlate) -> Self:
        return cls(
            uuid=model.uuid,
            size=model.size,
            name=model.name,
            external_ids=model.ids,
            model=model
        )

