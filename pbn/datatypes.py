from __future__ import annotations
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field

Color = Tuple[int, int, int]


@dataclass
class Segment:
    """Represents a single segment with pixels and optional metadata."""

    id: int
    pixels: List[Tuple[int, int]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SegmentedImage:
    """Container for segmented images with both label map and segment objects."""

    width: int
    height: int
    labels: List[List[int]]
    segments: List[Segment]
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_labels(cls, labels: List[List[int]]) -> "SegmentedImage":
        """Create SegmentedImage from a 2D label map, generating Segment objects."""
        height = len(labels)
        width = len(labels[0]) if height > 0 else 0

        segment_dict: Dict[int, List[Tuple[int, int]]] = {}
        for y, row in enumerate(labels):
            for x, seg_id in enumerate(row):
                segment_dict.setdefault(seg_id, []).append((x, y))

        segments = [Segment(id=sid, pixels=pixels) for sid, pixels in segment_dict.items()]
        return cls(width=width, height=height, labels=labels, segments=segments)

    @classmethod
    def from_segments(cls, segments: List[Segment], width: int, height: int) -> "SegmentedImage":
        """Create SegmentedImage from Segment objects, generating the label map."""
        labels: List[List[int]] = [[-1 for _ in range(width)] for _ in range(height)]
        for seg in segments:
            for x, y in seg.pixels:
                labels[y][x] = seg.id
        return cls(width=width, height=height, labels=labels, segments=segments)
