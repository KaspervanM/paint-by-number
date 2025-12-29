from .floyd_steinberg import FloydSteinbergDithering
from .registry import QAEnum, QA_MAP
from .nearest import NearestColorQuantization
from .base import ColorQuantizationAlgorithm

__all__ = [
    "QAEnum",
    "QA_MAP",
    "ColorQuantizationAlgorithm",
    "NearestColorQuantization",
    "FloydSteinbergDithering",
]