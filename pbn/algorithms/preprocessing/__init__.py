from .floyd_steinberg import FloydSteinbergDithering
from .no_preprocessing import NoPreprocessing
from .base import ImageProcessingAlgorithm

__all__ = [
    "ImageProcessingAlgorithm",
    "NoPreprocessing",
    "FloydSteinbergDithering",
]
