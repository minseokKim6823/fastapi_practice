from PIL import Image
from io import BytesIO
import base64

def get_image_size_from_base64(base64_string: str) -> tuple[int, int]:
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image.width, image.height