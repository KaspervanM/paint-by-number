from enum import StrEnum


class PreprocessingEnum(StrEnum):
    """Preprocessing Algorithm Enum"""

    NONE = "nop"
    FLOYD_STEINBERG = "floyd-steinberg"


class SegmentationEnum(StrEnum):
    """Segmentation Algorithm Enum"""

    GRID = "grid"
    VORONOI = "voronoi"
    KMEANS = "kmeans"
    WATERSHED = "watershed"
    LAB_WATERSHED = "lab_watershed"


class PostprocessingEnum(StrEnum):
    """Postprocessing Algorithm Enum"""

    NONE = "nop"
    MERGE = "merge"
    SMOOTH = "smooth"


class AssignmentEnum(StrEnum):
    """Assignment Algorithm Enum"""

    AVERAGE_NEAREST = "average-nearest"


class RenderingEnum(StrEnum):
    """Rendering Algorithm Enum"""

    COLORED = "colored"
