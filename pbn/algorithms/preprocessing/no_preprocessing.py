from typing import List, Optional
from PIL import Image

from .base import ImageProcessingAlgorithm
from pbn.datatypes import Color


class NoPreprocessing(ImageProcessingAlgorithm):
    """Color quantization using Floyd-Steinberg error diffusion dithering."""

    def process(self, image: Image.Image, palette: Optional[List[Color]] = None) -> Image.Image:
        """Do nothing."""
        return image
