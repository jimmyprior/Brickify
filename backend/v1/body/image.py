import io 
import os 
import base64

from PIL import Image 
from PIL.Image import Image as ImageType


def get_base64_from_pil_image(image : ImageType, img_format : str = "PNG") -> str:
    """
    image : Pillow image
    img_format : jpg, png (defaults to png)

    data:image/png;base64,{base64-goes-here}
    """
    buffer = io.BytesIO()
    image.save(buffer, img_format)
    return base64.b64encode(buffer.getvalue()).decode()


def get_pil_img_from_base64(base64_str : str) -> ImageType:
    """
    base64_str format: 
    takes a base64 string and returns pil image
    """
    return Image.open(
        io.BytesIO(
            base64.b64decode(base64_str)
        ) 
    ).convert("RGB")#need this or else issues when unpacking the rgb

class ImageModel(str): #have to keep this a str because PIL.Image.Image is not json sterizable
    # mosaic size is the image upload size 
    MAX_WIDTH = int(os.getenv("MAX_MOSAIC_WIDTH"))
    MAX_HEIGHT = int(os.getenv("MAX_MOSAIC_HEIGHT"))

    @classmethod
    def validate(cls, value, *args):
        #update to use pydantic version 2
        """Validate given base64 str to check if it is a valid image"""
        try: 
            image = get_pil_img_from_base64(str(value))
        except Exception as e:
            raise ValueError("Not a valid base64 image")
        #validate mosaic size within bounds
        if image.size[0] > ImageModel.MAX_WIDTH:
            raise ValueError(f"Image width can not exceed {ImageModel.MAX_WIDTH}")
        
        if image.size[1] > ImageModel.MAX_HEIGHT:
            raise ValueError(f"Image height can not exceed {ImageModel.MAX_HEIGHT}")
        #mosaic size must be a multiple of 16
        if (not image.size[0] % 16 == 0) or (not image.size[1] % 16 == 0):
            raise ValueError("Image width and height must be multiples of 16")
        
        image.base64 = value #make sure the image has the og base64 value 
        return image

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

