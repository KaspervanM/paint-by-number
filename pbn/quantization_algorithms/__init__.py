from .base import ColorQuantizationAlgorithm
from .floyd_steinberg import FloydSteinbergDithering
from .nearest import NearestColorQuantization

__all__ = [
    "ColorQuantizationAlgorithm",
    "NearestColorQuantization",
    "FloydSteinbergDithering",
]