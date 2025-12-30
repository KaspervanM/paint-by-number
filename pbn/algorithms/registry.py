from pbn.datatypes import PreprocessingEnum, SegmentationEnum, AssignmentEnum
from .preprocessing import FloydSteinbergDithering, NoPreprocessing
from .segmentation import GridSegmentation
from .assignment import AverageNearestColorAssignment

ALGORITHM_MAP = {
    PreprocessingEnum.NONE: NoPreprocessing,
    PreprocessingEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
    SegmentationEnum.GRID: GridSegmentation,
    AssignmentEnum.AVERAGE_NEAREST: AverageNearestColorAssignment,
}
