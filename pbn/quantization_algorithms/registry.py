from enum import Enum

from .floyd_steinberg import FloydSteinbergDithering
from .nearest import NearestColorQuantization


class QAEnum(str, Enum):
    """Quantization Algorithm Enum"""

    NEAREST = "nearest"
    FLOYD_STEINBERG = "floyd-steinberg"


"""Quantization Algorithm Map"""
QA_MAP = {
    QAEnum.NEAREST: NearestColorQuantization,
    QAEnum.FLOYD_STEINBERG: FloydSteinbergDithering,
}
