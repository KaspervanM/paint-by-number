import numpy as np
from PIL import Image
from scipy.spatial import distance
from typing import Optional

from pbn.datatypes import SegmentedImage
from .base import ImageSegmentationAlgorithm
from pbn.algorithms.enums import SegmentationEnum


class VoronoiImageSegmentation(ImageSegmentationAlgorithm):
    """Voronoi-based image segmentation using color and position.

    The points used are pixel coordinates and RGB-colors, creating a 5D space.
    Random points are selected (seeds) and segments are calculated based on these.
    Each point in the space is assigned to a seed if that seed is closest.
    A downside of the 5D approach is that segments are not necessarily contiguous
    in just its pixel coordinates. This results in seemingly more segments.
    """

    name = SegmentationEnum.VORONOI

    def __init__(
        self,
        num_seeds: int,
        spatial_weight: float = 1.0,
        color_weight: float = 1.0,
        seed: Optional[int] = None,
    ):
        self.params = {
            "num_seeds": num_seeds,
            "spatial_weight": spatial_weight,
            "color_weight": color_weight,
            "seed": seed,
        }

    def segment(self, image: Image.Image) -> SegmentedImage:
        if image.mode != "RGB":
            raise ValueError("Image must be RGB")

        rng = np.random.default_rng(self.params["seed"])
        pixels = np.array(image, dtype=float)
        height, width, _ = pixels.shape

        # Prepare pixel features: [x, y, r, g, b]
        xs, ys = np.meshgrid(np.arange(width), np.arange(height))
        xs = xs / width * self.params["spatial_weight"]
        ys = ys / height * self.params["spatial_weight"]
        colors = pixels / 255 * self.params["color_weight"]
        pixel_features = np.dstack((xs, ys, colors)).reshape(-1, 5)

        # Randomly pick seed points from all pixels
        seed_indices = rng.choice(len(pixel_features), self.params["num_seeds"], replace=False)
        seeds = pixel_features[seed_indices]

        # Compute nearest seed for each pixel (vectorized)
        dists = distance.cdist(pixel_features, seeds, metric="euclidean")
        labels_array = np.argmin(dists, axis=1).reshape(height, width)

        # Convert to list for type safety
        labels_list = labels_array.tolist()
        segmented = SegmentedImage.from_labels(labels_list)
        segmented.metadata.update(self.params)
        segmented.metadata["algorithm"] = "voronoi"

        return segmented
