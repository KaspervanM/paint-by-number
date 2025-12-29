from typing import List
from PIL import Image

from pbn.quantization_algorithms.base import ColorQuantizationAlgorithm
from pbn.datatypes import Color


class NearestColorQuantization(ColorQuantizationAlgorithm):
    """Trivial color quantization using nearest RGB distance."""

    name: str = "NearestColorQuantization"

    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Map each pixel to the nearest color in the palette."""
        image = image.convert("RGB")
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                pixels[x, y] = self._nearest_color(pixels[x, y], palette)

        return image
