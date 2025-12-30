from typing import Dict, Any
import pathlib


def serialize_params(params: Dict[str, Any]) -> str:
    """Serialize algorithm parameters into a filename-friendly string."""
    parts = []
    for k, v in params.items():
        if isinstance(v, (list, tuple)):
            val = "-".join(str(x) for x in v)
        else:
            val = str(v)
        parts.append(f"{k}-{val}")
    return "_".join(parts)


def make_output_filename(
    input_path: pathlib.Path,
    palette_path: pathlib.Path,
    pre_name: str,
    pre_params: Dict[str, Any],
    seg_name: str,
    seg_params: Dict[str, Any],
    assign_name: str,
    assign_params: Dict[str, Any],
) -> str:
    """Create a descriptive output filename based on input, palette, algorithms, and parameters."""
    parts = [input_path.stem, palette_path.stem]

    for name, params in [
        (pre_name, pre_params),
        (seg_name, seg_params),
        (assign_name, assign_params),
    ]:
        if name:
            parts.append(name)
        if params:
            parts.append(serialize_params(params))

    filename = "_".join(parts) + ".ppm"
    return filename


def resolve_output_path(
    input_path: pathlib.Path,
    palette_path: pathlib.Path,
    pre_name: str,
    pre_params: Dict[str, Any],
    seg_name: str,
    seg_params: Dict[str, Any],
    assign_name: str,
    assign_params: Dict[str, Any],
    output_dir: pathlib.Path,
) -> pathlib.Path:
    """Determine final output path, auto-generated in a directory."""
    filename = make_output_filename(
        input_path, palette_path, pre_name, pre_params, seg_name, seg_params, assign_name, assign_params
    )
    return output_dir / filename
