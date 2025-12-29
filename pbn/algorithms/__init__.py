from .floyd_steinberg import FloydSteinbergDithering
from .registry import AlgorithmEnum, ALGORITHM_MAP
from .nearest import NearestColorQuantization
from .base import ColorQuantizationAlgorithm

__all__ = [
    "AlgorithmEnum",
    "ALGORITHM_MAP",
    "ColorQuantizationAlgorithm",
    "NearestColorQuantization",
    "FloydSteinbergDithering",
]