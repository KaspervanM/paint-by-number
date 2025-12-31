from .preprocessing.base import ImageProcessingAlgorithm
from .segmentation.base import ImageSegmentationAlgorithm
from .assignment.base import ColorAssignmentAlgorithm
from .registry import ALGORITHM_MAP, PreprocessingEnum, SegmentationEnum, AssignmentEnum

__all__ = [
    "ALGORITHM_MAP",
    "ImageProcessingAlgorithm",
    "ImageSegmentationAlgorithm",
    "ColorAssignmentAlgorithm",
    "PreprocessingEnum",
    "SegmentationEnum",
    "AssignmentEnum",
]
