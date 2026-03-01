from io import BytesIO
from PIL import Image as PILImage
from PIL import ImageFilter


def blur_png_bytes(data: bytes, radius: int | float = 5) -> bytes:
    img = PILImage.open(BytesIO(data))
    blurred = img.filter(ImageFilter.GaussianBlur(radius))

    buf = BytesIO()
    blurred.save(buf, format="PNG")
    return buf.getvalue()
