from .preprocessing import FloydSteinbergDithering, NoPreprocessing
from .segmentation import GridImageSegmentation, VoronoiImageSegmentation, KMeansImageSegmentation
from .assignment import AverageNearestColorAssignment
from .enums import PreprocessingEnum, SegmentationEnum, AssignmentEnum


ALGORITHM_MAP = {
    PreprocessingEnum.NONE: NoPreprocessing,
    PreprocessingEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
    SegmentationEnum.GRID: GridImageSegmentation,
    SegmentationEnum.VORONOI: VoronoiImageSegmentation,
    SegmentationEnum.KMEANS: KMeansImageSegmentation,
    AssignmentEnum.AVERAGE_NEAREST: AverageNearestColorAssignment,
}
