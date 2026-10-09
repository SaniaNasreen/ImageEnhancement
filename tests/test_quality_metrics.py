import numpy as np
import pytest
from src.quality_metrics import assess_quality


def test_metrics_include_expected_fields():
    image = np.full((80, 120, 3), 180, dtype=np.uint8)
    result = assess_quality(image)
    assert result["width"] == 120
    assert result["height"] == 80
    assert "laplacian_variance" in result
    assert result["brightness_indicator"] == "mid_range"


def test_metrics_reject_empty_image():
    with pytest.raises(ValueError):
        assess_quality(np.array([]))
