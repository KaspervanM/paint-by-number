from typing import List
from PIL import Image

from pbn.quantization_algorithms import ColorQuantizationAlgorithm
from pbn.datatypes import Color


class PaintByNumber:
    """Paint-by-number image processor."""

    def __init__(self, palette: List[Color], algorithm: ColorQuantizationAlgorithm):
        """Initialize with a color palette and quantization algorithm."""
        self.palette = palette
        self.algorithm = algorithm

    def process(self, image: Image.Image) -> Image.Image:
        """Quantize an image to the configured color palette."""
        return self.algorithm.quantize(image, self.palette)
