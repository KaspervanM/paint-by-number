import numpy as np
from PIL import Image
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.morphology import h_minima
from skimage.feature import peak_local_max

from pbn.datatypes import SegmentedImage
from .base import ImageSegmentationAlgorithm
from pbn.algorithms.enums import SegmentationEnum


class WatershedImageSegmentation(ImageSegmentationAlgorithm):
    """Segment an image using marker-based watershed segmentation."""

    name = SegmentationEnum.WATERSHED

    def __init__(
        self, connectivity: int = 1, compactness: float = 0.0, min_distance: int = 10, h_minima_threshold: float = 0.1
    ):
        if connectivity not in (1, 2):
            raise ValueError("connectivity must be 1 or 2")
        if compactness < 0:
            raise ValueError("compactness must be non-negative")
        if min_distance < 1:
            raise ValueError("min_distance must be at least 1")
        if not 0 <= h_minima_threshold <= 1:
            raise ValueError("h_minima_threshold must be between 0 and 1")

        self.params = {
            "connectivity": connectivity,
            "compactness": compactness,
            "min_distance": min_distance,
            "h_minima_threshold": h_minima_threshold,
        }

    def segment(self, image: Image.Image) -> SegmentedImage:
        """Apply watershed segmentation to an RGB image."""
        if image.mode != "RGB":
            raise ValueError("Image must be RGB")

        img = np.asarray(image)
        gray = rgb2gray(img)
        gradient = sobel(gray)
        markers = self._generate_markers(gradient)

        labels_array = watershed(
            gradient, markers=markers, connectivity=self.params["connectivity"], compactness=self.params["compactness"]
        )

        labels_list = labels_array.tolist()
        segmented = SegmentedImage.from_labels(labels_list)
        segmented.metadata.update(self.params)
        segmented.metadata["algorithm"] = "watershed"
        segmented.metadata["num_segments"] = len(np.unique(labels_array))

        return segmented

    def _generate_markers(self, gradient: np.ndarray) -> np.ndarray:
        """Generate markers from local minima in gradient with h-minima suppression."""
        h = self.params["h_minima_threshold"] * (gradient.max() - gradient.min())

        if h > 0:
            gradient_processed = h_minima(gradient, h)
        else:
            gradient_processed = gradient

        local_max_coords = peak_local_max(
            -gradient_processed,
            min_distance=self.params["min_distance"],
            exclude_border=False,
        )

        markers = np.zeros_like(gradient, dtype=int)
        markers[tuple(local_max_coords.T)] = np.arange(1, len(local_max_coords) + 1)

        return markers
