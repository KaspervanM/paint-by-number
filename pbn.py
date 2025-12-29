from PIL import Image
from typing import List, Tuple, Protocol
import argparse
import pathlib
import math

Color = Tuple[int, int, int]


class ColorQuantizationAlgorithm(Protocol):
    """Protocol for color quantization algorithms."""

    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Quantize an image to a fixed color palette."""


class NearestColorQuantization:
    """Trivial color quantization using nearest RGB distance."""

    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Map each pixel to the nearest color in the palette."""
        image = image.convert("RGB")
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                pixels[x, y] = self._nearest_color(pixels[x, y], palette)

        return image

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return the palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))


class PaintByNumber:
    """Paint-by-number image processor."""

    def __init__(self, palette: List[Color], algorithm: ColorQuantizationAlgorithm):
        """Initialize with a color palette and quantization algorithm."""
        self.palette = palette
        self.algorithm = algorithm

    def process(self, image: Image.Image) -> Image.Image:
        """Quantize an image to the configured color palette."""
        return self.algorithm.quantize(image, self.palette)


def load_palette(path: pathlib.Path) -> List[Color]:
    """Load a color palette from a text file of R,G,B lines."""
    colors: List[Color] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            colors.append(tuple(map(int, line.split(","))))
    return colors


def main(image_path: pathlib.Path, palette_path: pathlib.Path) -> None:
    """Load an image and palette, apply paint-by-number quantization, and display it."""
    image = Image.open(image_path)
    palette = load_palette(palette_path)
    algorithm = NearestColorQuantization()
    pbn = PaintByNumber(palette, algorithm)
    result = pbn.process(image)
    result.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pbn",
        description="Paint by Number",
        epilog="Author: Kasper van Maasdam. Date: December 2025. Licence: GPL v3.0",
    )
    parser.add_argument(
        "input_image",
        type=pathlib.Path,
        help="Path to the image to turn into a paint by number.",
    )
    parser.add_argument(
        "palette",
        type=pathlib.Path,
        help="Path to a palette file containing R,G,B values per line.",
    )
    args = parser.parse_args()
    main(args.input_image, args.palette)
