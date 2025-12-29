from typing import Dict, Any, Optional
import pathlib


def serialize_params(qa_params: Dict[str, Any]) -> str:
    """Serialize algorithm parameters into a filename-friendly string."""
    parts = []
    for k, v in qa_params.items():
        if isinstance(v, (list, tuple)):
            val = "-".join(str(x) for x in v)
        else:
            val = str(v)
        parts.append(f"{k}-{val}")
    return "_".join(parts)


def make_output_filename(
    input_path: pathlib.Path, palette_path: pathlib.Path, qa_name: str, qa_params: Dict[str, Any]
) -> str:
    params_str = serialize_params(qa_params) if qa_params else ""
    parts = [input_path.stem, palette_path.stem, qa_name]
    if params_str:
        parts.append(params_str)
    filename = "_".join(parts) + ".ppm"
    return filename


def resolve_output_path(
    input_path: pathlib.Path,
    palette_path: pathlib.Path,
    qa_name: str,
    qa_params: Dict[str, Any],
    output_dir: pathlib.Path,
    output_file: Optional[pathlib.Path],
) -> pathlib.Path:
    if output_file:
        return output_file

    filename = make_output_filename(input_path, palette_path, qa_name, qa_params)
    return output_dir / filename
