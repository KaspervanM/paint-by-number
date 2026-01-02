from typing import Optional

from pbn.algorithms.enums import PreprocessingEnum
from .base import SegmentsProcessingAlgorithm
from pbn.datatypes import Palette, ColoredSegmentedImage


class NoPostprocessing(SegmentsProcessingAlgorithm):
    """Used to skip the postprocessing stage"""

    name = PreprocessingEnum.NONE

    def process(self, segments: ColoredSegmentedImage, palette: Optional[Palette] = None) -> ColoredSegmentedImage:
        """Do nothing."""
        return segments
