from .floyd_steinberg import FloydSteinbergDithering
from .nearest import NearestColorQuantization
from .base import ColorQuantizationAlgorithm

__all__ = [
    "ColorQuantizationAlgorithm",
    "NearestColorQuantization",
    "FloydSteinbergDithering",
]
