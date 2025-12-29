from enum import Enum

from .floyd_steinberg import FloydSteinbergDithering
from .nearest import NearestColorQuantization


class AlgorithmEnum(str, Enum):
    """Quantization Algorithm Enum"""

    NEAREST = "nearest"
    FLOYD_STEINBERG = "floyd-steinberg"


"""Quantization Algorithm Map"""
ALGORITHM_MAP = {
    AlgorithmEnum.NEAREST: NearestColorQuantization,
    AlgorithmEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
}
