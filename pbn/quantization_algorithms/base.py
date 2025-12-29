from abc import ABC, abstractmethod
from typing import List, Dict, Any
from PIL import Image
import math

from pbn.datatypes import Color


class ColorQuantizationAlgorithm(ABC):
    """Protocol for color quantization algorithms."""

    name: str = "BaseAlgorithm"

    params: Dict[str, Any] = {}

    @abstractmethod
    def quantize(self, image: Image.Image, palette: List[Color]) -> Image.Image:
        """Quantize an image to a fixed color palette."""
        pass

    def _nearest_color(self, color: Color, palette: List[Color]) -> Color:
        """Return the palette color with minimal Euclidean distance."""
        return min(palette, key=lambda p: self._distance(color, p))

    def _distance(self, a: Color, b: Color) -> float:
        """Compute Euclidean distance between two RGB colors."""
        return math.sqrt(sum((ac - bc) ** 2 for ac, bc in zip(a, b)))
