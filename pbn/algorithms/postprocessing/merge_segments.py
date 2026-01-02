from scipy.ndimage import label
from typing import Optional
import numpy as np

from pbn.algorithms.enums import PostprocessingEnum
from .base import SegmentsProcessingAlgorithm
from pbn.datatypes import Palette, ColoredSegment, ColoredSegmentedImage


class MergeSegments(SegmentsProcessingAlgorithm):
    """Segments with neighbors of the same color are merged into one larger segment."""

    name = PostprocessingEnum.MERGE

    def process(self, segments: ColoredSegmentedImage, palette: Optional[Palette] = None) -> ColoredSegmentedImage:
        """Merge adjacent segments of the same color."""
        labels = np.array(segments.labels)
        merged_segments: list[ColoredSegment] = []
        seg_id = 0

        for color in {seg.color for seg in segments.segments}:
            mask = np.zeros_like(labels, dtype=bool)
            for seg in segments.segments:
                if seg.color == color:
                    for x, y in seg.pixels:
                        mask[y, x] = True
            labeled_array, num_features = label(mask, structure=np.array([[1,1,1],[1,1,1],[1,1,1]]))
            for i in range(1, num_features + 1):
                pixels = list(zip(*np.where(labeled_array == i)[::-1]))
                merged_segments.append(ColoredSegment(id=seg_id, pixels=pixels, color=color))
                seg_id += 1

        return ColoredSegmentedImage.from_segments(merged_segments, width=segments.width, height=segments.height)
