import base64
from io import BytesIO

import easyocr
import numpy as np
from PIL.Image import Image

reader = easyocr.Reader(["pl", "en"])


def encode_pil_image(pil_image: Image) -> str:
    """
    Encode a PIL Image object to base64 without saving to disk

    Args:
        pil_image (PIL.Image.Image): The PIL Image object to encode

    Returns:
        str: Base64 encoded string of the image
    """
    buffered = BytesIO()
    # You can specify the format and quality here
    pil_image.convert("RGB").save(buffered, format="JPEG")
    # Get the byte data and encode it
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")


def get_text_from_img(image: Image) -> str:
    """
    Convert a PIL Image to string with easyocr

    Args:
        pil_image (PIL.Image.Image): The PIL Image object to encode

    Returns:
        str: text extracted from an image
    """
    # Convert PIL image to numpy array
    img_array = np.array(image)

    # Process with EasyOCR
    results = reader.readtext(img_array)

    # EasyOCR stubs are looser than runtime output; normalize to text explicitly.
    lines: list[str] = []
    for result in results:
        text_part = _extract_easyocr_text(result)
        if text_part:
            lines.append(text_part)

    return "\n".join(lines)


def _extract_easyocr_text(result: object) -> str:
    if isinstance(result, (list, tuple)) and len(result) > 1:
        text_value = result[1]
        return text_value if isinstance(text_value, str) else str(text_value)

    return ""
