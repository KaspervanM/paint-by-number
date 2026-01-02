from abc import ABC, abstractmethod
from PIL import Image
from typing import Any, Dict

from pbn.datatypes import Palette, SegmentedImage, ColoredSegmentedImage


class ColorAssignmentAlgorithm(ABC):
    """Abstract base class for algorithms that assign colors to segments in segmented images."""

    name: str
    params: Dict[str, Any] = {}

    @abstractmethod
    def assign_colors(self, image: Image.Image, segments: SegmentedImage, palette: Palette) -> ColoredSegmentedImage:
        """Assign a color from the palette to each segment and render."""
        pass
