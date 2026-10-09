"""Document-image enhancement operations."""
import cv2
import numpy as np


def _to_gray(image):
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("A non-empty image array is required.")
    if image.ndim == 2:
        return image.copy()
    if image.ndim == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    raise ValueError("Expected grayscale, BGR, or BGRA image.")


def enhance_image(image, mode="balanced"):
    """Enhance an image using classical computer-vision operations.

    balanced: denoise, CLAHE contrast enhancement, and gentle sharpening.
    grayscale: denoise and CLAHE, output grayscale.
    binary: grayscale, denoise, and adaptive thresholding.
    """
    if mode not in {"balanced", "grayscale", "binary"}:
        raise ValueError("mode must be balanced, grayscale, or binary")
    gray = _to_gray(image)
    denoised = cv2.fastNlMeansDenoising(gray, None, h=8, templateWindowSize=7, searchWindowSize=21)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrasted = clahe.apply(denoised)

    if mode == "binary":
        # Adaptive threshold works best for reasonably sized text/document images.
        block_size = min(31, min(contrasted.shape))
        if block_size % 2 == 0:
            block_size -= 1
        if block_size < 3:
            _, result = cv2.threshold(contrasted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return result
        return cv2.adaptiveThreshold(
            contrasted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, 11
        )
    if mode == "grayscale":
        return contrasted

    # Unsharp masking: original + scaled difference from a blurred version.
    softened = cv2.GaussianBlur(contrasted, (0, 0), sigmaX=1.2)
    sharpened = cv2.addWeighted(contrasted, 1.35, softened, -0.35, 0)
    return cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)

def create_comparison_image(original, enhanced):
    """
    Create a side-by-side comparison image.

    Parameters
    ----------
    original : np.ndarray
        Original input image.

    enhanced : np.ndarray
        Enhanced output image.

    Returns
    -------
    np.ndarray
        Combined comparison image.
    """

    # Make both images 3-channel
    if len(original.shape) == 2:
        original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)

    if len(enhanced.shape) == 2:
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    # Resize to same height
    h = max(original.shape[0], enhanced.shape[0])

    def resize_keep_ratio(img):
        scale = h / img.shape[0]
        w = int(img.shape[1] * scale)
        return cv2.resize(img, (w, h))

    original = resize_keep_ratio(original)
    enhanced = resize_keep_ratio(enhanced)

    comparison = np.hstack((original, enhanced))

    # Labels
    cv2.putText(
        comparison,
        "Original",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        comparison,
        "Enhanced",
        (original.shape[1] + 20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    return comparison