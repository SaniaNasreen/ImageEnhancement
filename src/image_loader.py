"""Input loading and validation helpers."""
from pathlib import Path
import cv2


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def load_image(path):
    """Load an image using OpenCV and reject missing or unsupported inputs."""
    image_path = Path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"Input image does not exist: {image_path}")
    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image extension '{image_path.suffix}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not decode image: {image_path}")
    if image.size == 0:
        raise ValueError(f"Image is empty: {image_path}")
    return image
