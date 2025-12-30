from typing import List, Optional
from PIL import Image

from pbn.algorithms.preprocessing import ImageProcessingAlgorithm
from pbn.algorithms.segmentation import ImageSegmentationAlgorithm
from pbn.algorithms.assignment import ColorAssignmentAlgorithm
from pbn.datatypes import Color


class PaintByNumber:
    """Orchestrates the paint-by-number pipeline with optional preprocessing, segmentation, and color assignment."""

    def __init__(
        self,
        palette: List[Color],
        preprocessing: ImageProcessingAlgorithm,
        segmentation: ImageSegmentationAlgorithm,
        assignment: ColorAssignmentAlgorithm,
    ):
        """Initialize the pipeline with palette and optional algorithms."""
        self.palette = palette
        self.preprocessing = preprocessing
        self.segmentation = segmentation
        self.assignment = assignment

    def process(self, image: Image.Image) -> Image.Image:
        """Run the full pipeline on the input image and return the processed image."""
        image = self.preprocessing.process(image, palette=self.palette)

        segments = (
            self.segmentation.segment(image)
            if self.segmentation
            else [[(x, y) for y in range(image.height)] for x in range(image.width)]
        )

        output_image = self.assignment.assign_colors(image, segments, self.palette) if self.assignment else image.copy()
        return output_image
