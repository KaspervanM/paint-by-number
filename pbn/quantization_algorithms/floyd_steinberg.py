from typing import List
from PIL import Image

from pbn.quantization_algorithms import ColorQuantizationAlgorithm
from pbn.datatypes import Color


class FloydSteinbergDithering(ColorQuantizationAlgorithm):
    """Color quantization using Floyd-Steinberg error diffusion dithering."""

    name: str = "FloydSteinbergDithering"

    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Quantize an image to the palette using Floyd-Steinberg dithering."""
        image = image.convert("RGB")
        pixels = image.load()
        width, height = image.size

        buffer = [[list(pixels[x, y]) for x in range(width)] for y in range(height)]

        for y in range(height):
            for x in range(width):
                old_pixel = buffer[y][x]
                new_pixel = self._nearest_color(tuple(int(c) for c in old_pixel), palette)
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
