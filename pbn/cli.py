from PIL import Image
import argparse
import pathlib

from pbn.algorithms import AlgorithmEnum, ALGORITHM_MAP
from pbn.output import resolve_output_path
from pbn.palette import load_palette
from pbn.core import PaintByNumber


def main() -> None:
    """Load an image and palette, apply paint-by-number quantization, and save the result."""
    parser = argparse.ArgumentParser(
        prog="pbn",
        description="Paint by Number is under development. Currently, it takes an input image and quantizes it according to the provided palette. The resulting image is PPM format.",
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
        "--algorithm",
        "-a",
        type=AlgorithmEnum,
        choices=list(AlgorithmEnum),
        default=AlgorithmEnum.FLOYD_STEINBERG,
        help="Color quantization algorithm to use.",
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
    image_path = args.input_image
    palette_path = args.palette
    output_dir = args.dir
    output_file = args.output

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

    result.save(output_path, format="PPM")


if __name__ == "__main__":
    main()
