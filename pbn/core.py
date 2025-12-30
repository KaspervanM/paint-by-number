from typing import Optional
from PIL import Image
import pathlib
import numpy as np
import skimage

from pbn.algorithms.preprocessing import ImageProcessingAlgorithm
from pbn.algorithms.segmentation import ImageSegmentationAlgorithm
from pbn.algorithms.assignment import ColorAssignmentAlgorithm
from pbn.output import resolve_intermediate_path
from pbn.algorithms import ALGORITHM_MAP
from pbn.palette import load_palette
from pbn.datatypes import Palette, PipelineRun, PipelineStageEnum, SegmentedImage


class PaintByNumber:
    """Orchestrates the paint-by-number pipeline with optional preprocessing, segmentation, and color assignment."""
    pipeline_run: PipelineRun
    palette: Palette
    preprocessing: ImageProcessingAlgorithm
    segmentation: ImageSegmentationAlgorithm
    assignment: ColorAssignmentAlgorithm
    intermediate_dir: Optional[pathlib.Path]

    def __init__(self, pipeline_run: PipelineRun):
        """Initialize the pipeline with palette and optional algorithms."""
        self.pipeline_run = pipeline_run
        self.palette = load_palette(pipeline_run.palette_path)
        self.preprocessing = ALGORITHM_MAP[pipeline_run.preprocessing_algorithm](**pipeline_run.preprocessing_params)
        self.segmentation = ALGORITHM_MAP[pipeline_run.segmentation_algorithm](**pipeline_run.segmentation_params)
        self.assignment = ALGORITHM_MAP[pipeline_run.assignment_algorithm](**pipeline_run.assignment_params)
        self.intermediate_dir = pipeline_run.intermediate_dir

    def process(self) -> Image.Image:
        """Run the full pipeline on the input image and return the processed image."""
        image = self.pipeline_run.original_image.copy()
        preprocessed_image = self.preprocessing.process(image, palette=self.palette)
        
        if self.intermediate_dir:
            output_path = resolve_intermediate_path(self.pipeline_run, PipelineStageEnum.PREPROCESSING)
            preprocessed_image.save(output_path)
            print(f"Saved intermediate image to: {output_path}")

        segments = self.segmentation.segment(preprocessed_image)

        if self.intermediate_dir:
            output_path = resolve_intermediate_path(self.pipeline_run, PipelineStageEnum.SEGMENTATION, "boundary-mask")
            boundary_mask = self._create_boundary_mask(segments)
            boundary_mask.save(output_path)
            print(f"Saved intermediate image to: {output_path}")

            output_path = resolve_intermediate_path(self.pipeline_run, PipelineStageEnum.SEGMENTATION, "boundary-overlay-original")
            self._overlay_boundaries(image, boundary_mask).save(output_path)
            print(f"Saved intermediate image to: {output_path}")

            output_path = resolve_intermediate_path(self.pipeline_run, PipelineStageEnum.SEGMENTATION, "boundary-overlay-preprocessed")
            self._overlay_boundaries(preprocessed_image, boundary_mask).save(output_path)
            print(f"Saved intermediate image to: {output_path}")

        output_image = self.assignment.assign_colors(preprocessed_image, segments, self.palette)
        return output_image
    
    def _create_boundary_mask(self, segments: SegmentedImage) -> Image.Image:
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
