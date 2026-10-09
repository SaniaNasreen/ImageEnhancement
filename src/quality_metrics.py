"""Explainable, no-training-required image quality indicators."""
import cv2
import numpy as np


def assess_quality(image):
    """Return simple image statistics.

    Laplacian variance is a blur *indicator*, not a universal quality score.
    Thresholds depend on image size, content, camera, and noise.
    """
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("A non-empty image array is required.")
    if image.ndim == 2:
        gray = image
    elif image.ndim == 3 and image.shape[2] in (3, 4):
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY if image.shape[2] == 4 else cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("Expected a grayscale, BGR, or BGRA image.")

    gray_float = gray.astype(np.float32)
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    mean_brightness = float(gray_float.mean())
    intensity_std = float(gray_float.std())
    # A deliberately documented heuristic; it should be calibrated for a dataset.
    blur_indicator = "possibly_blurry" if lap_var < 100.0 else "not_flagged_as_blurry"
    if mean_brightness < 70:
        brightness_indicator = "dark"
    elif mean_brightness > 190:
        brightness_indicator = "bright"
    else:
        brightness_indicator = "mid_range"
    if intensity_std < 25:
        contrast_indicator = "low_contrast"
    else:
        contrast_indicator = "contrast_not_flagged_low"

    height, width = gray.shape
    return {
        "width": int(width),
        "height": int(height),
        "channels": 1 if image.ndim == 2 else int(image.shape[2]),
        "mean_brightness": round(mean_brightness, 4),
        "intensity_std": round(intensity_std, 4),
        "laplacian_variance": round(lap_var, 4),
        "blur_indicator": blur_indicator,
        "brightness_indicator": brightness_indicator,
        "contrast_indicator": contrast_indicator,
    }
