from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from pbn.datatypes import Palette, ColoredSegmentedImage


class SegmentsProcessingAlgorithm(ABC):
    """Abstract base class for segments processing algorithms."""

    name: str
    params: Dict[str, Any] = {}

    @abstractmethod
    def process(self, segments: ColoredSegmentedImage, palette: Optional[Palette] = None) -> ColoredSegmentedImage:
        """Transform colored segments. E.g. smooth boundaries, merge. Palette is required only for palette-dependent algorithms."""
        pass
