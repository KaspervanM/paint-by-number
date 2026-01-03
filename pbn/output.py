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


def make_intermediate_filename(pipeline_run: PipelineRun, stage: PipelineStageEnum, step: int, notes: str) -> str:
    """Generate a descriptive filename for an intermediate stage."""
    parts = [pipeline_run.input_path.stem, pipeline_run.palette_path.stem, stage]

    if notes:
        parts.append(notes)

    for i, preprocessing_algo in enumerate(pipeline_run.preprocessing):
        if stage == PipelineStageEnum.PREPROCESSING and i > step:
            break
        parts.append(preprocessing_algo.name)
        if preprocessing_algo.params:
            parts.append(serialize_params(preprocessing_algo.params))

    if stage in (PipelineStageEnum.SEGMENTATION, PipelineStageEnum.POSTPROCESSING):
        parts.append(pipeline_run.segmentation.name)
        if pipeline_run.segmentation.params:
            parts.append(serialize_params(pipeline_run.segmentation.params))

    if stage == PipelineStageEnum.POSTPROCESSING:
        for i, postprocessing_algo in enumerate(pipeline_run.postprocessing):
            if i > step:
                break
            parts.append(postprocessing_algo.name)
            if postprocessing_algo.params:
                parts.append(serialize_params(postprocessing_algo.params))

    if stage in (PipelineStageEnum.COLOR_ASSINGMENT, PipelineStageEnum.RENDERING):
        raise ValueError("Unsupported stage.")

    return "_".join(parts) + ".ppm"


def resolve_intermediate_path(pipeline_run: PipelineRun, stage: PipelineStageEnum, step: int = 0, notes: str = "") -> pathlib.Path:
    """Determine final output path, auto-generated in a directory."""
    if not pipeline_run.intermediate_dir:
        raise RuntimeError("An intermediate image path cannot be created without a provided directory.")

    return pipeline_run.intermediate_dir / make_intermediate_filename(pipeline_run, stage, step, notes)


def make_output_filename(pipeline_run: PipelineRun) -> str:
    """Create a descriptive output filename based on input, palette, algorithms, and parameters."""
    parts = [pipeline_run.input_path.stem, pipeline_run.palette_path.stem]

    for preprocessing_algo in pipeline_run.preprocessing:
        parts.append(preprocessing_algo.name)
        if preprocessing_algo.params:
            parts.append(serialize_params(preprocessing_algo.params))

    parts.append(pipeline_run.segmentation.name)
    if pipeline_run.segmentation.params:
        parts.append(serialize_params(pipeline_run.segmentation.params))

    for postprocessing_algo in pipeline_run.postprocessing:
        parts.append(postprocessing_algo.name)
        if postprocessing_algo.params:
            parts.append(serialize_params(postprocessing_algo.params))

    parts.append(pipeline_run.assignment.name)
    if pipeline_run.assignment.params:
        parts.append(serialize_params(pipeline_run.assignment.params))

    filename = "_".join(parts) + ".ppm"
    return filename


def resolve_output_path(pipeline_run: PipelineRun, output_dir: pathlib.Path) -> pathlib.Path:
    """Determine final output path, auto-generated in a directory."""
    return output_dir / make_output_filename(pipeline_run)
