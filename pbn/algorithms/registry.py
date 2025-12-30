from enum import Enum

from .preprocessing import FloydSteinbergDithering, NoPreprocessing
from .segmentation import GridSegmentation
from .assignment import AverageNearestColorAssignment


class PreprocessingEnum(str, Enum):
    """Preprocessing Algorithm Enum"""

    NONE = "no-preprocessing"
    FLOYD_STEINBERG = "floyd-steinberg"


class SegmentationEnum(str, Enum):
    """Segmentation Algorithm Enum"""

    GRID = "grid-segmentation"


class AssignmentEnum(str, Enum):
    """Assignment Algorithm Enum"""

    AVERAGE_NEAREST = "average-nearest"


ALGORITHM_MAP = {
    PreprocessingEnum.NONE: NoPreprocessing,
    PreprocessingEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
    SegmentationEnum.GRID: GridSegmentation,
    AssignmentEnum.AVERAGE_NEAREST: AverageNearestColorAssignment,
}
