from typing import Optional, cast
import numpy as np
from scipy.ndimage import label, grey_closing, grey_opening

from pbn.algorithms.enums import PostprocessingEnum
from .base import SegmentsProcessingAlgorithm
from pbn.datatypes import Palette, ColoredSegment, ColoredSegmentedImage


class SmoothBoundaries(SegmentsProcessingAlgorithm):
    """Smooths segment boundaries using morphological operations."""

    name = PostprocessingEnum.SMOOTH

    def __init__(self, iterations: int = 1, kernel_size: int = 3, kernel_shape: str = "disk"):
        self.params = {
            "iterations": iterations,
            "kernel_size": kernel_size,
            "kernel_shape": kernel_shape,
        }

    def process(self, segments: ColoredSegmentedImage, palette: Optional[Palette] = None) -> ColoredSegmentedImage:
        """Apply morphological smoothing to segment boundaries."""
        labels = np.array(segments.labels)
        height, width = labels.shape
        
        kernel_size: int = cast(int, self.params["kernel_size"])
        
        structure = np.array([[1,1,1],[1,1,1],[1,1,1]])
        
        unique_colors = list({seg.color for seg in segments.segments})
        color_to_id = {color: idx for idx, color in enumerate(unique_colors)}
        
        color_map = np.full((height, width), -1, dtype=int)
        for seg in segments.segments:
            color_id = color_to_id[seg.color]
            for x_, y_ in seg.pixels:
                color_map[y_, x_] = color_id
        
        if self.params["kernel_shape"] == "disk":
            y, x = np.ogrid[-kernel_size:kernel_size+1, -kernel_size:kernel_size+1]
            kernel = x**2 + y**2 <= kernel_size**2
        else:
            kernel = np.ones((kernel_size, kernel_size), dtype=bool)
        
        smoothed_map = color_map.astype(float)
        for _ in range(self.params["iterations"]):
            smoothed_map = grey_closing(smoothed_map, footprint=kernel)
            smoothed_map = grey_opening(smoothed_map, footprint=kernel)
        smoothed_map = smoothed_map.astype(int)
        
        merged_segments: list[ColoredSegment] = []
        seg_id = 0
        
        for color_id, color in enumerate(unique_colors):
            mask = smoothed_map == color_id
            labeled_array, num_features = label(mask, structure=structure)
            
            for i in range(1, num_features + 1):
                ys, xs = np.where(labeled_array == i)
                pixels = list(zip(xs, ys))
                merged_segments.append(ColoredSegment(id=seg_id, pixels=pixels, color=color))
                seg_id += 1
        
        return ColoredSegmentedImage.from_segments(merged_segments, width=width, height=height)
