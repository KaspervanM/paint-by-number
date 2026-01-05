from __future__ import annotations
from typing import List, Tuple, Dict, Any, Optional, Sequence, cast, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import StrEnum
from PIL import Image
from abc import ABC, abstractmethod
import pathlib

if TYPE_CHECKING:
    from pbn.algorithms import (
        ImageProcessingAlgorithm,
        ImageSegmentationAlgorithm,
        SegmentsProcessingAlgorithm,
        ColorAssignmentAlgorithm,
        SegmentRenderingAlgorithm,
    )

Color = Tuple[int, int, int]

Palette = List[Color]


class PipelineStageEnum(StrEnum):
    PREPROCESSING = "preprocessing"
    SEGMENTATION = "segmentation"
    COLOR_ASSINGMENT = "color-assignment"
    POSTPROCESSING = "postprocessing"
    RENDERING = "rendering"


@dataclass
class PipelineRun:
    """Encapsulates all metadata and objects for a single PaintByNumber pipeline execution."""

    input_path: pathlib.Path
    original_image: Image.Image
    palette_path: pathlib.Path

    preprocessing: List[ImageProcessingAlgorithm]
    segmentation: ImageSegmentationAlgorithm
    postprocessing: List[SegmentsProcessingAlgorithm]
    assignment: ColorAssignmentAlgorithm
    rendering: SegmentRenderingAlgorithm

    intermediate_dir: Optional[pathlib.Path] = None


@dataclass
class Segment:
    """Represents a single segment with pixel coordinates."""

    id: int
    pixels: List[Tuple[int, int]]


@dataclass
class ColoredSegment(Segment):
    """Represents a segment with an associated RGB color."""

    color: Color


@dataclass
class BaseSegmentedImage(ABC):
    """Base class for segmented images with common logic."""

    width: int
    height: int
    segments: Sequence[Segment]
    labels: List[List[int]] = field(init=False)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Check IDs, generate label map, and enforce no overlaps."""
        self._check_unique_ids()
        self._generate_labels()

    def _check_unique_ids(self) -> None:
        """Ensure all segment IDs are unique."""
        ids = [seg.id for seg in self.segments]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate segment IDs detected")

    def _generate_labels(self) -> None:
        """Generate label map and check for overlapping pixels."""
        labels: List[List[int]] = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        for seg in self.segments:
            for x, y in seg.pixels:
                if labels[y][x] != -1:
                    raise ValueError(f"Pixel ({x}, {y}) belongs to multiple segments")
                labels[y][x] = seg.id
        self.labels = labels

    @abstractmethod
    def copy(self) -> BaseSegmentedImage:
        pass


@dataclass
class SegmentedImage(BaseSegmentedImage):
    """Container for standard segmented images with non-colored segments."""

    @classmethod
    def from_labels(cls, labels: List[List[int]]) -> SegmentedImage:
        """Create SegmentedImage from a 2D label map."""
        height = len(labels)
        width = len(labels[0]) if height > 0 else 0
        segment_dict: Dict[int, List[Tuple[int, int]]] = {}
        for y, row in enumerate(labels):
            for x, seg_id in enumerate(row):
                segment_dict.setdefault(seg_id, []).append((x, y))
        segments = [Segment(id=sid, pixels=pixels) for sid, pixels in segment_dict.items()]
        return cls(width=width, height=height, segments=segments)

    @classmethod
    def from_segments(cls, segments: Sequence[Segment], width: int, height: int) -> SegmentedImage:
        """Create SegmentedImage from Segment objects."""
        return cls(width=width, height=height, segments=segments)

    def copy(self) -> SegmentedImage:
        return SegmentedImage(
            width=self.width,
            height=self.height,
            segments=[Segment(id=seg.id, pixels=list(seg.pixels)) for seg in self.segments],
            metadata=dict(self.metadata),
        )


@dataclass
class ColoredSegmentedImage(BaseSegmentedImage):
    """Container for segmented images with colored segments."""

    segments: Sequence[ColoredSegment]

    @classmethod
    def from_segments(
        cls,
        segments: Sequence[ColoredSegment] | Sequence[Segment] | BaseSegmentedImage,
        width: int,
        height: int,
        color_map: Optional[Dict[int, Color]] = None,
    ) -> ColoredSegmentedImage:
        """
        Create ColoredSegmentedImage from ColoredSegment objects or Segment objects with a color_map.
        """
        if isinstance(segments, BaseSegmentedImage):
            if isinstance(segments, SegmentedImage):
                segments = segments.segments
            elif isinstance(segments, ColoredSegmentedImage) and not color_map:
                return segments.copy()
            elif color_map:
                segments = segments.copy().segments
            else:
                raise TypeError()
        if all(isinstance(seg, ColoredSegment) for seg in segments) and not color_map:
            colored_segments: List[ColoredSegment] = list(cast(Sequence[ColoredSegment], segments))
        else:
            if color_map is None:
                raise TypeError("Segments are not ColoredSegment. Must provide a color_map: Dict[segment_id, Color]")
            colored_segments = []
            for seg in segments:
                if seg.id not in color_map:
                    raise ValueError(f"No color provided for segment id {seg.id}")
                colored_segments.append(ColoredSegment(id=seg.id, pixels=seg.pixels, color=color_map[seg.id]))

        return cls(width=width, height=height, segments=colored_segments)

    def copy(self) -> ColoredSegmentedImage:
        return ColoredSegmentedImage(
            width=self.width,
            height=self.height,
            segments=[ColoredSegment(id=seg.id, pixels=list(seg.pixels), color=seg.color) for seg in self.segments],
            metadata=dict(self.metadata),
        )
