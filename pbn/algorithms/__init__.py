from .quantization import ColorQuantizationAlgorithm, NearestColorQuantization, FloydSteinbergDithering
from .registry import AlgorithmEnum, ALGORITHM_MAP

__all__ = [
    "AlgorithmEnum",
    "ALGORITHM_MAP",
    "ColorQuantizationAlgorithm",
    "NearestColorQuantization",
    "FloydSteinbergDithering",
]
