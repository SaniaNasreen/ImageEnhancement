import numpy as np
import pytest
from src.enhancement import enhance_image


def test_enhancement_preserves_dimensions():
    image = np.full((80, 100, 3), 200, dtype=np.uint8)
    result = enhance_image(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_binary_mode_returns_grayscale():
    image = np.random.default_rng(1).integers(0, 256, (80, 100, 3), dtype=np.uint8)
    result = enhance_image(image, mode="binary")
    assert result.shape == (80, 100)


def test_invalid_mode_fails():
    with pytest.raises(ValueError):
        enhance_image(np.zeros((10, 10), dtype=np.uint8), mode="wrong")
