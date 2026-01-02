from .preprocessing import FloydSteinbergDithering, NoPreprocessing
from .segmentation import GridImageSegmentation, VoronoiImageSegmentation, KMeansImageSegmentation, WatershedImageSegmentation, LABWatershedSegmentation
from .postprocessing import MergeSegments, NoPostprocessing
from .assignment import AverageNearestColorAssignment
from .rendering import ColoredRendering
from .enums import PreprocessingEnum, SegmentationEnum, PostprocessingEnum, AssignmentEnum, RenderingEnum


ALGORITHM_MAP = {
    PreprocessingEnum.NONE: NoPreprocessing,
    PreprocessingEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
    SegmentationEnum.GRID: GridImageSegmentation,
    SegmentationEnum.VORONOI: VoronoiImageSegmentation,
    SegmentationEnum.KMEANS: KMeansImageSegmentation,
    SegmentationEnum.WATERSHED: WatershedImageSegmentation,
    SegmentationEnum.LAB_WATERSHED: LABWatershedSegmentation,
    PostprocessingEnum.NONE: NoPostprocessing,
    PostprocessingEnum.MERGE: MergeSegments,
    AssignmentEnum.AVERAGE_NEAREST: AverageNearestColorAssignment,
    RenderingEnum.COLORED: ColoredRendering,
}
