"""
Configuration values used throughout ImageClarity.

All thresholds are heuristic values chosen for this educational project.
If the application is evaluated on a different dataset, these values may
need to be adjusted.
"""

# ----------------------------
# Brightness Thresholds
# ----------------------------

LOW_BRIGHTNESS = 70
HIGH_BRIGHTNESS = 190

# ----------------------------
# Contrast Thresholds
# ----------------------------

LOW_CONTRAST_STD = 25

# ----------------------------
# Blur Threshold
# ----------------------------

LAPLACIAN_BLUR_THRESHOLD = 100

# ----------------------------
# Image Quality Score Weights
# ----------------------------

BRIGHTNESS_WEIGHT = 25
CONTRAST_WEIGHT = 25
BLUR_WEIGHT = 30
NOISE_WEIGHT = 20
TOTAL_SCORE = (
    BRIGHTNESS_WEIGHT
    + CONTRAST_WEIGHT
    + BLUR_WEIGHT
    + NOISE_WEIGHT
)

# ----------------------------
# Enhancement Parameters
# ----------------------------

CLAHE_CLIP_LIMIT = 2.0
CLAHE_TILE_SIZE = (8, 8)

DENOISE_STRENGTH = 8

SHARPEN_AMOUNT = 1.35
SHARPEN_BLUR = 0.35