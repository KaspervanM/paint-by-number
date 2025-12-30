from abc import ABC, abstractmethod
from PIL import Image
from typing import Any, Dict, List

from pbn.datatypes import Color


class ColorAssignmentAlgorithm(ABC):
    """Abstract base class for algorithms that assign colors to segments in segmented images."""

    params: Dict[str, Any] = {}

    @abstractmethod
    def assign_colors(self, image: Image.Image, segments: Any, palette: List[Color]) -> Image.Image:
        """Assign a color from the palette to each segment and render."""
        pass
