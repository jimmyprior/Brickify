from uuid import UUID
from typing import Self

from brickpy import Color

from ..database.color import ColorStandard, ExternalIDs


class BrickifyColor(Color):
    """
    
    """
    def __init__(
        self, 
        uuid : UUID,
        external_ids : ExternalIDs,
        lab : tuple[float], 
        rgb : tuple[float], 
        name : str,
        model : ColorStandard
        ):
        super().__init__(lab, rgb, name)
        self.uuid = uuid
        self.external_ids = external_ids
        self.model = model

    @classmethod
    def from_model(cls : Self, model : ColorStandard) -> Self:
        return cls(
            uuid=model.uuid, 
            external_ids=model.ids, 
            lab=model.spaces.cielab, 
            rgb=model.spaces.rgb,
            name=model.name,
            model=model
        )
    
