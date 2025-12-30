from typing import Dict, Any
import pathlib

from pbn.datatypes import PipelineRun, PipelineStageEnum


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


def make_intermediate_filename(pipeline_run: PipelineRun, stage: PipelineStageEnum, notes: str = "") -> str:
    """Generate a descriptive filename for an intermediate stage."""
    parts = [pipeline_run.input_path.stem, pipeline_run.palette_path.stem, stage]

    if notes:
        parts.append(notes)

    if pipeline_run.preprocessing_algorithm:
        parts.append(pipeline_run.preprocessing_algorithm)
    if pipeline_run.preprocessing_params:
        parts.append(serialize_params(pipeline_run.preprocessing_params))

    match stage:
        case PipelineStageEnum.PREPROCESSING:
            pass
        case PipelineStageEnum.SEGMENTATION:
            if pipeline_run.segmentation_algorithm:
                parts.append(pipeline_run.segmentation_algorithm)
            if pipeline_run.segmentation_params:
                parts.append(serialize_params(pipeline_run.segmentation_params))
        case _:
            raise ValueError("Unsupported stage.")

    return "_".join(parts) + ".ppm"


def resolve_intermediate_path(pipeline_run: PipelineRun, stage: PipelineStageEnum, notes: str = "") -> pathlib.Path:
    """Determine final output path, auto-generated in a directory."""
    if not pipeline_run.intermediate_dir:
        raise RuntimeError("An intermediate image path cannot be created without a provided directory.")

    return pipeline_run.intermediate_dir / make_intermediate_filename(pipeline_run, stage, notes)


def make_output_filename(pipeline_run: PipelineRun) -> str:
    """Create a descriptive output filename based on input, palette, algorithms, and parameters."""
    parts = [pipeline_run.input_path.stem, pipeline_run.palette_path.stem]

    for name, params in [
        (pipeline_run.preprocessing_algorithm, pipeline_run.preprocessing_params),
        (pipeline_run.segmentation_algorithm, pipeline_run.segmentation_params),
        (pipeline_run.assignment_algorithm, pipeline_run.assignment_params),
    ]:
        if name:
            parts.append(name)
        if params:
            parts.append(serialize_params(params))

    filename = "_".join(parts) + ".ppm"
    return filename


def resolve_output_path(pipeline_run: PipelineRun, output_dir: pathlib.Path) -> pathlib.Path:
    """Determine final output path, auto-generated in a directory."""
    return output_dir / make_output_filename(pipeline_run)
