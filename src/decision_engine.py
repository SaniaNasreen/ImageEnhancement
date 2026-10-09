"""
Decision engine for ImageClarity.

This module analyses image-quality metrics and recommends which
enhancement operations should be applied.
"""

from src.config import (
    LOW_BRIGHTNESS,
    HIGH_BRIGHTNESS,
    LOW_CONTRAST_STD,
    LAPLACIAN_BLUR_THRESHOLD,
)


def recommend_pipeline(metrics):
    """
    Recommend enhancement operations.

    Parameters
    ----------
    metrics : dict
        Dictionary returned by assess_quality().

    Returns
    -------
    dict
        {
            "operations": [...],
            "recommendations": [...]
        }
    """

    operations = []
    recommendations = []

    brightness = metrics["mean_brightness"]
    contrast = metrics["intensity_std"]
    blur = metrics["laplacian_variance"]

    # Brightness
    if brightness < LOW_BRIGHTNESS:
        operations.append("increase_brightness")
        recommendations.append("Image is dark.")

    elif brightness > HIGH_BRIGHTNESS:
        operations.append("reduce_brightness")
        recommendations.append("Image is too bright.")

    # Contrast
    if contrast < LOW_CONTRAST_STD:
        operations.append("clahe")
        recommendations.append("Low contrast detected.")

    # Blur
    if blur < LAPLACIAN_BLUR_THRESHOLD:
        operations.append("sharpen")
        recommendations.append("Image appears blurry.")

    # Default
    if not operations:
        recommendations.append(
            "Image quality looks acceptable. Only standard enhancement will be applied."
        )
        operations.append("balanced")

    return {
        "operations": operations,
        "recommendations": recommendations,
    }