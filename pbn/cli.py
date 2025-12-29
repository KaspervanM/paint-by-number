from PIL import Image
import argparse
import pathlib

from pbn.algorithms import AlgorithmEnum, ALGORITHM_MAP
from pbn.output import resolve_output_path
from pbn import PaintByNumber, load_palette


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
        choices=list(map(lambda x: x.value, AlgorithmEnum)),
        default=AlgorithmEnum.NEAREST,
        help=f"Color quantization algorithm to use. Default: {AlgorithmEnum.NEAREST}.",
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
    image_path = args.input_image.resolve()
    palette_path = args.palette.resolve()
    qa_name = args.algorithm
    output_dir = args.dir.resolve()
    output_file = args.output.resolve() if args.output else None

    if not output_dir.is_dir():
        raise NotADirectoryError(f"{output_dir} does not exist or is not a directory")
    if output_file:
        parent_dir = output_file.parent
        if not parent_dir.exists():
            raise FileNotFoundError(f"Directory for output file does not exist: {parent_dir}")

    with Image.open(image_path) as image:
        palette = load_palette(palette_path)
        quantization_algorithm = ALGORITHM_MAP[qa_name]()
        pbn = PaintByNumber(palette, quantization_algorithm)
        result = pbn.process(image)

        output_path = resolve_output_path(
            image_path, palette_path, qa_name, quantization_algorithm.params, output_dir, output_file
        )

        result.save(output_path, format="PPM")
        print(f"Saved output image to: {output_path}")


if __name__ == "__main__":
    main()
