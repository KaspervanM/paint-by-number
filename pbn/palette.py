from typing import List
import pathlib

from pbn.datatypes import Color


def load_palette(path: pathlib.Path) -> List[Color]:
    """Load a color palette from a text file of R,G,B lines."""
    colors: List[Color] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            colors.append(tuple(map(int, line.split(","))))
    return colors
