from PIL import Image

from pbn.datatypes import ColoredSegmentedImage
from pbn.algorithms.enums import RenderingEnum
from .base import SegmentRenderingAlgorithm


class ColoredRendering(SegmentRenderingAlgorithm):
    """Abstract base class for segment rendering algorithms."""

    name = RenderingEnum.COLORED

    def render(self, colored_segments: ColoredSegmentedImage) -> Image.Image:
        """Render the colored segments by coloring in the segments."""
        output = Image.new("RGB", (colored_segments.width, colored_segments.height))
        out_pixels = output.load()
        if out_pixels is None:
            raise ValueError("Failed to load image pixels.")

        for segment in colored_segments.segments:
            for x, y in segment.pixels:
                out_pixels[x, y] = segment.color

        return output