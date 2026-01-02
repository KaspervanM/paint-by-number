from typing import List, Dict, Any
from PIL import Image
import math

from pbn.datatypes import Palette, Color, SegmentedImage, Segment, ColoredSegmentedImage
from .base import ColorAssignmentAlgorithm
from pbn.algorithms.enums import AssignmentEnum


class AverageNearestColorAssignment(ColorAssignmentAlgorithm):
    """Assigns each segment the palette color closest to its average color."""

    name = AssignmentEnum.AVERAGE_NEAREST

    @staticmethod
    def average_color(segment: Segment, src_pixels: Any) -> Color:
        """Compute average RGB color of a segment."""
        r = g = b = 0
        n = len(segment.pixels)

        for x, y in segment.pixels:
            pr, pg, pb = src_pixels[x, y]
            r += pr
            g += pg
            b += pb

        return (r // n, g // n, b // n)

    def assign_colors(
        self,
        image: Image.Image,
        segments: SegmentedImage,
        palette: Palette,
    ) -> ColoredSegmentedImage:
        """Compute average segment colors and assign nearest palette color."""
        image = image.convert("RGB")
        src_pixels = image.load()
        if src_pixels is None:
            raise ValueError("Failed to load image pixels.")

        color_map: Dict[int, Color] = {}

        for segment in segments.segments:
            avg_color = self.average_color(segment, src_pixels)
            assigned = self._nearest_color(avg_color, palette)

            color_map[segment.id] = assigned

        return ColoredSegmentedImage.from_segments(segments, image.width, image.height, color_map)

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))
