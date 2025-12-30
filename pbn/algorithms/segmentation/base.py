from abc import ABC, abstractmethod
from typing import Any, Dict
from PIL import Image

from pbn.datatypes import SegmentedImage


class ImageSegmentationAlgorithm(ABC):
    """Abstract base class for image segmentation algorithms."""

    params: Dict[str, Any] = {}

    @abstractmethod
    def segment(self, image: Image.Image) -> SegmentedImage:
        """Segment an image into regions (return labels, masks, polygons, etc.)."""
        pass
