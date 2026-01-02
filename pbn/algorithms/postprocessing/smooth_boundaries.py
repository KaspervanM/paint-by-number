from typing import Optional

from pbn.algorithms.enums import PostprocessingEnum
from .base import SegmentsProcessingAlgorithm
from pbn.datatypes import Palette, ColoredSegmentedImage


class SmoothBoundaries(SegmentsProcessingAlgorithm):
    """Used to skip the postprocessing stage"""

    name = PostprocessingEnum.SMOOTH

    def process(self, segments: ColoredSegmentedImage, palette: Optional[Palette] = None) -> ColoredSegmentedImage:
        """Do nothing."""
        return segments