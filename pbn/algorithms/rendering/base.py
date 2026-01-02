from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from PIL import Image

from pbn.datatypes import Color, ColoredSegmentedImage


class SegmentRenderingAlgorithm(ABC):
    """Abstract base class for segment rendering algorithms."""

    name: str
    params: Dict[str, Any] = {}

    @abstractmethod
    def render(self, colored_segments: ColoredSegmentedImage) -> Image.Image | Tuple[Image.Image, Dict[int, Color]]:
        """Render the colored segments. E.g. add color numbers for each segment or render colored image.
        Returns image and optionally a color map."""
        pass
