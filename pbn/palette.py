import pathlib

from pbn.datatypes import Palette


def load_palette(path: pathlib.Path) -> Palette:
    """Load a color palette from a text file of R,G,B lines, allowing comments after '#'."""
    palette: Palette = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Remove any inline comment after '#'
            line = line.split("#", 1)[0].strip()

            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Invalid color line: '{line}'. Must have exactly 3 values.")

            r_str, g_str, b_str = parts
            r, g, b = int(r_str), int(g_str), int(b_str)
            palette.append((r, g, b))
    return palette
