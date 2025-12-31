import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from typing import Optional

from pbn.datatypes import SegmentedImage
from .base import ImageSegmentationAlgorithm
from pbn.algorithms.enums import SegmentationEnum


class KMeansImageSegmentation(ImageSegmentationAlgorithm):
    """Image segmentation using k-means clustering on color and position.
    
    The points used are pixel coordinates and RGB-colors, creating a 5D space.
    A downside of the 5D approach is that segments are not necessarily contiguous
    in just its pixel coordinates. This results in seemingly more segments.
    """

    name = SegmentationEnum.KMEANS

    def __init__(
        self,
        num_clusters: int,
        spatial_weight: float = 1.0,
        color_weight: float = 1.0,
        seed: Optional[int] = None,
    ):
        self.params = {
            "num_clusters": num_clusters,
            "spatial_weight": spatial_weight,
            "color_weight": color_weight,
            "seed": seed,
        }

    def segment(self, image: Image.Image) -> SegmentedImage:
        """Segment an image into regions (return labels, masks, polygons, etc.)."""
        if image.mode != "RGB":
            raise ValueError("Image must be RGB")

        pixels = np.array(image, dtype=float)
        height, width, _ = pixels.shape

        # Generate grid of coordinates
        xs, ys = np.meshgrid(np.arange(width), np.arange(height))
        xs = xs / width * self.params["spatial_weight"]
        ys = ys / height * self.params["spatial_weight"]

        # Normalize colors and apply color weight
        colors = pixels / 255 * self.params["color_weight"]

        # Stack features: [x, y, r, g, b]
        features = np.dstack((xs, ys, colors))
        flat_features = features.reshape(-1, 5)

        # Fit k-means using library
        kmeans = KMeans(
            n_clusters=self.params["num_clusters"],
            random_state=self.params["seed"],
            n_init=10,
        )
        kmeans.fit(flat_features)
        labels_array = kmeans.labels_.reshape(height, width)

        # Convert to list for type safety
        labels_list = labels_array.tolist()
        segmented = SegmentedImage.from_labels(labels_list)
        segmented.metadata.update(self.params)
        segmented.metadata["algorithm"] = "kmeans"

        return segmented
