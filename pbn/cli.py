from PIL import Image
import argparse
import pathlib
from typing import Optional

from pbn import PaintByNumber, load_palette
from pbn.algorithms import PreprocessingEnum, SegmentationEnum, AssignmentEnum, ALGORITHM_MAP
from pbn.output import resolve_output_path


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
        "-c",
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

    args = parser.parse_args()

    input_path: pathlib.Path = args.input_image.resolve()
    palette_path: pathlib.Path = args.palette.resolve()
    output_dir: pathlib.Path = args.dir.resolve()
    output_file: Optional[pathlib.Path] = args.output.resolve() if args.output else None

    if not output_dir.is_dir():
        raise NotADirectoryError(f"{output_dir} does not exist or is not a directory")
    if output_file and not output_file.parent.exists():
        raise FileNotFoundError(f"Directory for output file does not exist: {output_file.parent}")

    with Image.open(input_path) as image:
        palette = load_palette(palette_path)
        preprocessing = ALGORITHM_MAP[args.preprocessing]()
        segmentation = ALGORITHM_MAP[args.segmentation]()
        assignment = ALGORITHM_MAP[args.assignment]()

        pbn = PaintByNumber(
            palette=palette,
            preprocessing=preprocessing,
            segmentation=segmentation,
            assignment=assignment,
        )

        result = pbn.process(image)

        output_path = (
            resolve_output_path(
                input_path,
                palette_path,
                args.preprocessing.value,
                preprocessing.params,
                args.segmentation.value,
                segmentation.params,
                args.assignment.value,
                assignment.params,
                output_dir,
            )
            if not output_file
            else output_file
        )

        result.save(output_path, format="PPM")
        print(f"Saved output image to: {output_path}")


if __name__ == "__main__":
    main()
