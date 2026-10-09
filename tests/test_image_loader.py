import pytest
from src.image_loader import load_image


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_image("this_file_should_not_exist.png")
