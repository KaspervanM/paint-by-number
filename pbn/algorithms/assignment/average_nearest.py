from typing import List
from PIL import Image
import math

from pbn.datatypes import Color, SegmentedImage, Segment
from .base import ColorAssignmentAlgorithm


class AverageNearestColorAssignment(ColorAssignmentAlgorithm):
    """Assigns each segment the palette color closest to its average color."""

    def __init__(self):
        """Initialize average nearest color assignment."""
        self.params = {}

    def assign_colors(
        self,
        image: Image.Image,
        segments: SegmentedImage,
        palette: List[Color],
    ) -> Image.Image:
        """Compute average segment colors and assign nearest palette color."""
        image = image.convert("RGB")
        src_pixels = image.load()

        output = Image.new("RGB", (segments.width, segments.height))
        out_pixels = output.load()
        if out_pixels is None:
            raise ValueError("Failed to load image pixels.")

        for segment in segments.segments:
            avg_color = self._average_color(segment, src_pixels)
            assigned = self._nearest_color(avg_color, palette)

            for x, y in segment.pixels:
                out_pixels[x, y] = assigned

        return output

    def _average_color(self, segment: Segment, src_pixels) -> Color:
        """Compute average RGB color of a segment."""
        r = g = b = 0
        n = len(segment.pixels)

        for x, y in segment.pixels:
            pr, pg, pb = src_pixels[x, y]
            r += pr
            g += pg
            b += pb

        return (r // n, g // n, b // n)

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))
