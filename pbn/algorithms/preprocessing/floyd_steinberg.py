from typing import List, Optional, cast, Tuple
from PIL import Image
import math

from .base import ImageProcessingAlgorithm
from pbn.datatypes import Color


class FloydSteinbergDithering(ImageProcessingAlgorithm):
    """Color quantization using Floyd-Steinberg error diffusion dithering."""

    def process(self, image: Image.Image, palette: Optional[List[Color]] = None) -> Image.Image:
        """Transform the image. E.g. blur, dither. Palette is required only for palette-dependent algorithms like dithering."""
        if not palette:
            raise ValueError("Palette required for dithering.")

        image = image.convert("RGB")
        pixels = image.load()
        if pixels is None:
            raise ValueError("Failed to load image pixels.")

        width, height = image.size

        buffer: list[list[list[float]]] = [
            [list(map(float, cast(Tuple[int, int, int], pixels[x, y]))) for x in range(width)] for y in range(height)
        ]

        for y in range(height):
            for x in range(width):
                old_pixel = buffer[y][x]
                r, g, b = map(int, old_pixel)
                new_pixel = self._nearest_color((r, g, b), palette)
                pixels[x, y] = new_pixel
                error = [old_pixel[i] - new_pixel[i] for i in range(3)]

                if x + 1 < width:
                    buffer[y][x + 1] = [buffer[y][x + 1][i] + error[i] * 7 / 16 for i in range(3)]
                if x - 1 >= 0 and y + 1 < height:
                    buffer[y + 1][x - 1] = [buffer[y + 1][x - 1][i] + error[i] * 3 / 16 for i in range(3)]
                if y + 1 < height:
                    buffer[y + 1][x] = [buffer[y + 1][x][i] + error[i] * 5 / 16 for i in range(3)]
                if x + 1 < width and y + 1 < height:
                    buffer[y + 1][x + 1] = [buffer[y + 1][x + 1][i] + error[i] * 1 / 16 for i in range(3)]

        return image

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return the palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))
