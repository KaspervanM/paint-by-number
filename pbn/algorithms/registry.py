from .preprocessing import FloydSteinbergDithering, NoPreprocessing
from .segmentation import GridImageSegmentation, VoronoiImageSegmentation, KMeansImageSegmentation, WatershedImageSegmentation, LABWatershedSegmentation
from .assignment import AverageNearestColorAssignment
from .enums import PreprocessingEnum, SegmentationEnum, AssignmentEnum


ALGORITHM_MAP = {
    PreprocessingEnum.NONE: NoPreprocessing,
    PreprocessingEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
    SegmentationEnum.GRID: GridImageSegmentation,
    SegmentationEnum.VORONOI: VoronoiImageSegmentation,
    SegmentationEnum.KMEANS: KMeansImageSegmentation,
    SegmentationEnum.WATERSHED: WatershedImageSegmentation,
    SegmentationEnum.LAB_WATERSHED: LABWatershedSegmentation,
    AssignmentEnum.AVERAGE_NEAREST: AverageNearestColorAssignment,
}
