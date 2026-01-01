from typing import Optional, Type, Tuple, Dict, Any, Callable
from enum import Enum
from PIL import Image
import argparse
import pathlib

from pbn import PaintByNumber
from pbn.algorithms import PreprocessingEnum, SegmentationEnum
from pbn.output import resolve_output_path
from pbn.algorithms import AssignmentEnum
from pbn.algorithms import ALGORITHM_MAP
from pbn.datatypes import PipelineRun


def parse_enum_with_params(enum_cls: Type[Enum]) -> Callable[[str], Tuple[Enum, Dict[str, Any]]]:
    """The type that parses the algorithm with parameters provided over the CLI"""

    def parser(value: str) -> Tuple[Enum, Dict[str, Any]]:
        parts = value.split(",")
        name = parts[0]

        try:
            enum_value = enum_cls(name)
        except ValueError:
            valid = ", ".join(e.value for e in enum_cls)
            raise argparse.ArgumentTypeError(f"Invalid value '{name}'. Choose from: {valid}")

        params: Dict[str, Any] = {}
        for part in parts[1:]:
            if "=" not in part:
                raise argparse.ArgumentTypeError(f"Invalid parameter '{part}'. Expected key=value.")
            val: str | int | float | bool | None
            key, val = part.split("=", 1)

            if val == "None":
                val = None
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            else:
                try:
                    val = float(val)
                except ValueError:
                    pass

            params[key] = val

        return enum_value, params

    return parser


def main() -> None:
    """Load an image and palette, run the paint-by-number pipeline, and save the result."""
    parser = argparse.ArgumentParser(
        prog="pbn",
        description="Paint by Number: Convert images to a palette-based representation. The resulting image is in PPM format.",
        epilog="Author: Kasper van Maasdam. Date: December 2025. Licence: GPL v3.0",
    )

    parser.add_argument("input_image", type=pathlib.Path, help="path to the input image")
    parser.add_argument("palette", type=pathlib.Path, help="path to palette file (R,G,B per line)")
    parser.add_argument(
        "-p",
        "--preprocessing",
        type=parse_enum_with_params(PreprocessingEnum),
        default=(PreprocessingEnum.NONE, {}),
        help=(
            "preprocessing algorithm and parameters. "
            f"Options: {{{', '.join(e.value for e in PreprocessingEnum)}}}. "
            "Default: nop"
        ),
    )
    parser.add_argument(
        "-s",
        "--segmentation",
        type=parse_enum_with_params(SegmentationEnum),
        default=(SegmentationEnum.GRID, {"cell_size": 1}),
        help=(
            "segmentation algorithm and parameters. "
            f"Options: {{{', '.join(e.value for e in SegmentationEnum)}}}. "
            "Default: grid,cell_size=1"
        ),
    )
    parser.add_argument(
        "-a",
        "--assignment",
        type=parse_enum_with_params(AssignmentEnum),
        default=(AssignmentEnum.AVERAGE_NEAREST, {}),
        help=(
            "color assignment algorithm to map palette colors to segments. "
            f"Options: {{{', '.join(e.value for e in AssignmentEnum)}}}. "
            "Default: average-nearest"
        ),
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="directory to save the output image. Default: current directory",
    )
    parser.add_argument(
        "--output", "-o", type=pathlib.Path, help="exact output file path and overrides --dir if provided"
    )
    parser.add_argument(
        "--intermediate-images",
        "-i",
        type=pathlib.Path,
        help="enables storing intermediate images by providing directory where to store them",
    )

    args = parser.parse_args()

    input_path: pathlib.Path = args.input_image.resolve()
    palette_path: pathlib.Path = args.palette.resolve()
    output_dir: pathlib.Path = args.dir.resolve()
    output_file: Optional[pathlib.Path] = args.output.resolve() if args.output else None
    intermediate_dir: Optional[pathlib.Path] = args.intermediate_images.resolve() if args.intermediate_images else None

    if not output_dir.is_dir():
        raise NotADirectoryError(f"{output_dir} does not exist or is not a directory")
    if output_file and not output_file.parent.is_dir():
        raise NotADirectoryError(f"{output_file.parent} does not exist or is not a directory")
    if intermediate_dir and not intermediate_dir.is_dir():
        raise NotADirectoryError(f"{intermediate_dir} does not exist or is not a directory")

    with Image.open(input_path) as image:
        pipeline_run = PipelineRun(
            input_path=input_path,
            original_image=image.copy(),
            palette_path=palette_path,
            preprocessing=ALGORITHM_MAP[args.preprocessing[0]](**args.preprocessing[1]),
            segmentation=ALGORITHM_MAP[args.segmentation[0]](**args.segmentation[1]),
            assignment=ALGORITHM_MAP[args.assignment[0]](**args.assignment[1]),
            intermediate_dir=intermediate_dir,
        )

        pbn = PaintByNumber(pipeline_run)

        result = pbn.process()

        output_path = resolve_output_path(pipeline_run, output_dir) if not output_file else output_file

        result.save(output_path, format="PPM")
        print(f"Saved output image to: {output_path}")


if __name__ == "__main__":
    main()
