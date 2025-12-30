from PIL import Image
import argparse
import pathlib
from typing import Optional

from pbn import PaintByNumber
from pbn.algorithms import PreprocessingEnum, SegmentationEnum, AssignmentEnum
from pbn.output import resolve_output_path
from pbn.datatypes import PipelineRun


def main() -> None:
    """Load an image and palette, run the paint-by-number pipeline, and save the result."""
    parser = argparse.ArgumentParser(
        prog="pbn",
        description="Paint by Number: Convert images to a palette-based representation. The resulting image is in PPM format.",
        epilog="Author: Kasper van Maasdam. Date: December 2025. Licence: GPL v3.0",
    )

    parser.add_argument("input_image", type=pathlib.Path, help="Path to the input image.")
    parser.add_argument("palette", type=pathlib.Path, help="Path to palette file (R,G,B per line).")
    parser.add_argument(
        "-p",
        "--preprocessing",
        type=PreprocessingEnum,
        choices=[e.value for e in PreprocessingEnum],
        default=PreprocessingEnum.NONE,
        help="Preprocessing algorithm (optional).",
    )
    parser.add_argument(
        "-s",
        "--segmentation",
        type=SegmentationEnum,
        choices=[e.value for e in SegmentationEnum],
        default=SegmentationEnum.GRID,
        help="Segmentation algorithm to split the image into regions.",
    )
    parser.add_argument(
        "-a",
        "--assignment",
        type=AssignmentEnum,
        choices=[e.value for e in AssignmentEnum],
        default=AssignmentEnum.AVERAGE_NEAREST,
        help="Color assignment algorithm to map palette colors to segments.",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help=f"Directory to save the output image. Default: current directory ({pathlib.Path.cwd()}).",
    )
    parser.add_argument(
        "--output", "-o", type=pathlib.Path, help="Exact output file path. Overrides --dir if provided."
    )
    parser.add_argument(
        "--intermediate-images",
        type=pathlib.Path,
        help="Directory where to store intermediate images. For debugging or development purposes. If not provided, no intermediate images will be generated.",
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
            preprocessing_algorithm=args.preprocessing,
            preprocessing_params={},
            segmentation_algorithm=args.segmentation,
            segmentation_params={"cell_size": 30},
            assignment_algorithm=args.assignment,
            assignment_params={},
            intermediate_dir=intermediate_dir,
        )

        pbn = PaintByNumber(pipeline_run)

        result = pbn.process()

        output_path = resolve_output_path(pipeline_run, output_dir) if not output_file else output_file

        result.save(output_path, format="PPM")
        print(f"Saved output image to: {output_path}")


if __name__ == "__main__":
    main()
