from typing import Optional
from PIL import Image

from pbn.algorithms.enums import PreprocessingEnum
from .base import ImageProcessingAlgorithm
from pbn.datatypes import Palette


class NoPreprocessing(ImageProcessingAlgorithm):
    """Used to skip the preprocessing stage."""

    name = PreprocessingEnum.NONE

    def process(self, image: Image.Image, palette: Optional[Palette] = None) -> Image.Image:
        """Do nothing."""
        return image
