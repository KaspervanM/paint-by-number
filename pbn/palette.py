import pathlib
import re

from pbn.datatypes import Palette


HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def load_palette(path: pathlib.Path) -> Palette:
    """Load a color palette from RGB or hex color lines."""
    palette: Palette = []
    with path.open() as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            token = line.split(maxsplit=1)[0]

            if HEX_RE.match(token):
                r = int(token[1:3], 16)
                g = int(token[3:5], 16)
                b = int(token[5:7], 16)
                palette.append((r, g, b))
                continue

            if token.startswith("#"):
                continue

            parts = token.split(",")
            if len(parts) != 3:
                raise ValueError(f"Invalid color line: '{raw_line.rstrip()}'")

            r, g, b = map(int, parts)
            palette.append((r, g, b))

    return palette
