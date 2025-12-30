from typing import List, Tuple
from PIL import Image

from pbn.datatypes import SegmentedImage, Segment
from .base import ImageSegmentationAlgorithm


class GridSegmentation(ImageSegmentationAlgorithm):
    """Segments an image into a regular grid of square pixel blocks."""

    def __init__(self, cell_size: int):
        """Initialize grid segmentation with a given square cell size."""
        if cell_size < 1:
            raise ValueError("cell_size must be >= 1")
        self.cell_size = cell_size
        self.params = {"cell_size": cell_size}

    def segment(self, image: Image.Image) -> SegmentedImage:
        """Segment the image into grid-aligned square regions."""
        width, height = image.size

        labels: List[List[int]] = [[-1 for _ in range(width)] for _ in range(height)]
        segments: List[Segment] = []

        segment_id = 0
        for y0 in range(0, height, self.cell_size):
            for x0 in range(0, width, self.cell_size):
                pixels: List[Tuple[int, int]] = []

                for y in range(y0, min(y0 + self.cell_size, height)):
                    for x in range(x0, min(x0 + self.cell_size, width)):
                        labels[y][x] = segment_id
                        pixels.append((x, y))

                segments.append(Segment(id=segment_id, pixels=pixels))
                segment_id += 1

        return SegmentedImage(
            width=width,
            height=height,
            labels=labels,
            segments=segments,
            metadata={"type": "grid"},
        )
