"""Optional skew estimation and correction using dominant text-like edges."""
import cv2
import numpy as np


def estimate_skew_angle(image):
    """Estimate a modest document skew angle in degrees; return 0 if uncertain."""
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("A non-empty image array is required.")
    gray = image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 1800, threshold=60,
                            minLineLength=max(20, gray.shape[1] // 8), maxLineGap=15)
    if lines is None:
        return 0.0
    angles = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = map(int, line)
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if -20 <= angle <= 20:
            angles.append(float(angle))
    if not angles:
        return 0.0
    # Median resists a few non-text edges; this is a heuristic, not document segmentation.
    return float(np.median(angles))


def correct_skew(image, angle=None):
    """Rotate image to compensate for estimated skew while preserving canvas size."""
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("A non-empty image array is required.")
    angle = estimate_skew_angle(image) if angle is None else float(angle)
    if abs(angle) < 0.15:
        return image.copy()
    height, width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)
    return cv2.warpAffine(image, matrix, (width, height), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)
