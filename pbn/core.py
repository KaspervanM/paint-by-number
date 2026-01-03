from typing import Optional, Dict, Tuple, List
from PIL import Image
import pathlib
import numpy as np
import skimage

from pbn.algorithms import (
    ImageProcessingAlgorithm,
    ImageSegmentationAlgorithm,
    SegmentsProcessingAlgorithm,
    ColorAssignmentAlgorithm,
    SegmentRenderingAlgorithm,
    PreprocessingEnum,
    PostprocessingEnum,
)
from pbn.algorithms.assignment import AverageNearestColorAssignment
from pbn.algorithms.rendering import ColoredRendering
from pbn.output import resolve_intermediate_path
from pbn.palette import load_palette
from pbn.datatypes import Color, Palette, PipelineRun, PipelineStageEnum, BaseSegmentedImage, ColoredSegmentedImage


class PaintByNumber:
    """Orchestrates the paint-by-number pipeline with optional preprocessing, segmentation, and color assignment."""

    pipeline_run: PipelineRun
    palette: Palette
    preprocessing: List[ImageProcessingAlgorithm]
    segmentation: ImageSegmentationAlgorithm
    postprocessing: List[SegmentsProcessingAlgorithm]
    assignment: ColorAssignmentAlgorithm
    rendering: SegmentRenderingAlgorithm
    intermediate_dir: Optional[pathlib.Path]

    def __init__(self, pipeline_run: PipelineRun):
        """Initialize the pipeline with palette and optional algorithms."""
        self.pipeline_run = pipeline_run
        self.palette = load_palette(pipeline_run.palette_path)
        self.preprocessing = pipeline_run.preprocessing
        self.segmentation = pipeline_run.segmentation
        self.postprocessing = pipeline_run.postprocessing
        self.assignment = pipeline_run.assignment
        self.rendering = pipeline_run.rendering
        self.intermediate_dir = pipeline_run.intermediate_dir

    def process(self) -> Image.Image | Tuple[Image.Image, Dict[int, Color]]:
        """Run the full pipeline on the input image and return the processed image."""
        image = self.pipeline_run.original_image.copy()

        preprocessed_image = image.copy()

        for step, preprocessing_algo in enumerate(self.preprocessing):
            preprocessed_image = preprocessing_algo.process(preprocessed_image, self.palette)

            if self.intermediate_dir and preprocessing_algo.name != PreprocessingEnum.NONE:
                output_path = resolve_intermediate_path(self.pipeline_run, PipelineStageEnum.PREPROCESSING, step)
                preprocessed_image.save(output_path)
                print(f"Saved intermediate image to: {output_path}")

        segments = self.segmentation.segment(preprocessed_image)

        if self.intermediate_dir:
            self._save_intermediate_segments(
                PipelineStageEnum.SEGMENTATION, self.segmentation.name, image, preprocessed_image, segments
            )

        colored_segments = self.assignment.assign_colors(preprocessed_image, segments, self.palette)

        processed_segments = colored_segments.copy()

        for step, postprocessing_algo in enumerate(self.postprocessing):
            processed_segments = postprocessing_algo.process(processed_segments, self.palette)

            if self.intermediate_dir and postprocessing_algo.name != PostprocessingEnum.NONE:
                self._save_intermediate_segments(
                    PipelineStageEnum.POSTPROCESSING,
                    postprocessing_algo.name,
                    image,
                    preprocessed_image,
                    processed_segments,
                    step,
                )

        rendering_output = self.rendering.render(processed_segments)
        return rendering_output

    def _save_intermediate_segments(
        self,
        stage: PipelineStageEnum,
        algorithm_name: str,
        base_image: Image.Image,
        preprocessed_image: Image.Image,
        segments: BaseSegmentedImage,
        step: int = 0,
    ) -> None:
        output_path = resolve_intermediate_path(self.pipeline_run, stage, step, "boundary-mask")
        boundary_mask = self._create_boundary_mask(segments)
        boundary_mask.save(output_path)
        print(f"Saved intermediate image to: {output_path}")

        output_path = resolve_intermediate_path(self.pipeline_run, stage, step, "boundary-overlay-original")
        self._overlay_boundaries(base_image, boundary_mask).save(output_path)
        print(f"Saved intermediate image to: {output_path}")

        output_path = resolve_intermediate_path(self.pipeline_run, stage, step, "segments-average-original")
        self._segements_average_color_image(base_image, segments).save(output_path)
        print(f"Saved intermediate image to: {output_path}")

        if self.preprocessing and not all([p.name == PreprocessingEnum.NONE for p in self.preprocessing]):
            output_path = resolve_intermediate_path(self.pipeline_run, stage, step, "boundary-overlay-preprocessed")
            self._overlay_boundaries(preprocessed_image, boundary_mask).save(output_path)
            print(f"Saved intermediate image to: {output_path}")

            output_path = resolve_intermediate_path(self.pipeline_run, stage, step, "segments-average-preprocessed")
            self._segements_average_color_image(preprocessed_image, segments).save(output_path)
            print(f"Saved intermediate image to: {output_path}")

    def _create_boundary_mask(self, segments: BaseSegmentedImage) -> Image.Image:
        """Create a black-and-white mask of segment boundaries."""
        labels = np.array(segments.labels)
        boundaries = skimage.segmentation.find_boundaries(labels, mode="outer")
        mask_array = np.zeros(labels.shape, dtype=np.uint8)
        mask_array[boundaries] = 255
        return Image.fromarray(mask_array, mode="L")

    def _overlay_boundaries(self, base_image: Image.Image, boundary_mask: Image.Image) -> Image.Image:
        """Overlay segment boundaries on a base image using a mask."""
        white = Image.new("RGB", base_image.size, (255, 255, 255))
        blended = Image.blend(base_image, white, alpha=0.5)
        return Image.composite(blended, base_image, boundary_mask.convert("L"))

    def _segements_average_color(self, base_image: Image.Image, segments: BaseSegmentedImage) -> ColoredSegmentedImage:
        base_image = base_image.convert("RGB")
        src_pixels = base_image.load()
        if src_pixels is None:
            raise ValueError("Failed to load image pixels.")

        color_map: Dict[int, Color] = {}

        for segment in segments.segments:
            color_map[segment.id] = AverageNearestColorAssignment.average_color(segment, src_pixels)

        return ColoredSegmentedImage.from_segments(segments, base_image.width, base_image.height, color_map)

    def _segements_average_color_image(self, base_image: Image.Image, segments: BaseSegmentedImage) -> Image.Image:
        colored_segments = self._segements_average_color(base_image, segments)

        return ColoredRendering().render(colored_segments)
