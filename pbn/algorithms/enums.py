from enum import Enum


class PreprocessingEnum(str, Enum):
    """Preprocessing Algorithm Enum"""

    NONE = "nop"
    FLOYD_STEINBERG = "floyd-steinberg"


class SegmentationEnum(str, Enum):
    """Segmentation Algorithm Enum"""

    GRID = "grid"
    VORONOI = "voronoi"
    KMEANS = "kmeans"
    WATERSHED = "watershed"
    LAB_WATERSHED= "lab_watershed"


class AssignmentEnum(str, Enum):
    """Assignment Algorithm Enum"""

    AVERAGE_NEAREST = "average-nearest"
