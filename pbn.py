from PIL import Image
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional
import argparse
import pathlib
import math

Color = Tuple[int, int, int]


class ColorQuantizationAlgorithm(ABC):
    """Protocol for color quantization algorithms."""

    name: str = "BaseAlgorithm"

    params: Dict[str, Any] = {}

    @abstractmethod
    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Quantize an image to a fixed color palette."""
        pass

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return the palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))


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


class FloydSteinbergDithering(ColorQuantizationAlgorithm):
    """Color quantization using Floyd–Steinberg error diffusion dithering."""

    name: str = "FloydSteinbergDithering"

    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Quantize an image to the palette using Floyd–Steinberg dithering."""
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


def serialize_params(params: Dict[str, Any]) -> str:
    """Serialize algorithm parameters into a filename-friendly string."""
    parts = []
    for k, v in params.items():
        if isinstance(v, (list, tuple)):
            val = "-".join(str(x) for x in v)
        else:
            val = str(v)
        parts.append(f"{k}-{val}")
    return "_".join(parts)


def make_output_filename(
    input_path: pathlib.Path, palette_path: pathlib.Path, algorithm: ColorQuantizationAlgorithm
) -> str:
    params_str = serialize_params(algorithm.params) if algorithm.params else ""
    parts = [input_path.stem, palette_path.stem, algorithm.name]
    if params_str:
        parts.append(params_str)
    filename = "_".join(parts) + input_path.suffix
    return filename


def resolve_output_path(
    input_path: pathlib.Path,
    palette_path: pathlib.Path,
    algorithm: ColorQuantizationAlgorithm,
    output_dir: pathlib.Path,
    output_file: Optional[pathlib.Path],
) -> pathlib.Path:
    if output_file:
        return output_file

    filename = make_output_filename(input_path, palette_path, algorithm)
    return output_dir / filename


def main(
    image_path: pathlib.Path, palette_path: pathlib.Path, output_dir: pathlib.Path, output_file: Optional[pathlib.Path]
) -> None:
    """Load an image and palette, apply paint-by-number quantization, and display it."""
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
    if not output_dir.is_dir():
        raise NotADirectoryError(f"Specified --dir is not a directory: {output_dir}")
    if output_file:
        parent_dir = output_file.parent
        if not parent_dir.exists():
            raise FileNotFoundError(f"Directory for output file does not exist: {parent_dir}")

    image = Image.open(image_path)
    palette = load_palette(palette_path)
    algorithm = FloydSteinbergDithering()
    pbn = PaintByNumber(palette, algorithm)
    result = pbn.process(image)

    output_path = resolve_output_path(image_path, palette_path, algorithm, output_dir, output_file)

    result.save(output_path)


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
    parser.add_argument(
        "--dir",
        "-d",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help=f"Directory where the output image will be saved. Default: current directory ('{pathlib.Path.cwd()}').",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=pathlib.Path,
        help="Exact output file path. Overrides --dir if provided. If not provided, a name will be automatically generated.",
    )
    args = parser.parse_args()
    main(args.input_image, args.palette, args.dir, args.output)
