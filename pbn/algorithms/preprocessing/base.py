from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from PIL import Image

from pbn.datatypes import Color


class ImageProcessingAlgorithm(ABC):
    """Abstract base class for image processing algorithms."""

    params: Dict[str, Any] = {}

    @abstractmethod
    def process(self, image: Image.Image, palette: Optional[List[Color]] = None) -> Image.Image:
        """Transform the image. E.g. blur, dither. Palette is required only for palette-dependent algorithms like dithering."""
        pass
