# Paint by Number

**Paint by Number** is a Python tool that converts images into paint-by-number style outputs using a fixed color palette. The project is currently **under development** and not usable yet.

## Features

- Quantize images to a fixed palette of colors
- Supports multiple quantization algorithms (nearest color, Floyd-Steinberg dithering)
- Modular, extensible architecture for adding new algorithms and experimentation

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/KaspervanM/paint-by-number.git
cd paint-by-number
pip install -e .
```

For development, run `pip install -e .[dev]` instead.

Dependencies will be installed automatically.

## Running the CLI

You can run the tool in several ways:

### 1. Using the installed console command

After installing with `pip install -e .` or `pip install -e .[dev]`:

```bash
pbn my_image.png my_palette.txt
```

### 2. Using the module

You could use:

```bash
python3 -m pbn.cli my_image.png my_palette.txt
```

But option 1 is recommended.

### Usage

```
usage: pbn [-h] [-p PREPROCESSING] [-s SEGMENTATION] [-a ASSIGNMENT] [-t POSTPROCESSING] [-r RENDERING] [--dir DIR] [--output OUTPUT]
           [--intermediate-images INTERMEDIATE_IMAGES]
           input_image palette

Paint by Number: Convert images to a palette-based representation. The resulting image is in PPM format.

positional arguments:
  input_image           path to the input image
  palette               path to palette file (R,G,B per line)

options:
  -h, --help            show this help message and exit
  -p, --preprocessing PREPROCESSING
                        preprocessing algorithm and parameters. Options: {nop, floyd-steinberg}. Default: nop. Can be specified multiple times to
                        chain algorithms.
  -s, --segmentation SEGMENTATION
                        segmentation algorithm and parameters. Options: {grid, voronoi, kmeans, watershed, lab_watershed}. Default:
                        grid,cell_size=1
  -a, --assignment ASSIGNMENT
                        color assignment algorithm to map palette colors to segments. Options: {average-nearest}. Default: average-nearest
  -t, --postprocessing POSTPROCESSING
                        segmentation postprocessing algorithm and parameters. Options: {nop, merge, smooth}. Default: merge. Can be specified
                        multiple times to chain algorithms.
  -r, --rendering RENDERING
                        rendering algorithm to render segments. E.g. colored image or numbered image. Options: {colored}. Default: color
  --dir, -d DIR         directory to save the output image. Default: current directory
  --output, -o OUTPUT   exact output file path and overrides --dir if provided
  --intermediate-images, -i INTERMEDIATE_IMAGES
                        enables storing intermediate images by providing directory where to store them

Author: Kasper van Maasdam. Date: December 2025. License: GPL v3.0
```

## Notes

The project is a work in progress. So far, a pipeline has been constructed that consists of the following stages:

1. preprocessing (image -> image)
2. segmentation (image -> segments)
4. color-assignment (segments -> colored segments)
3. postprocessing (colored segments -> colored segments)
5. rendering (colored segments -> image)

The idea is that the preprocessing contains stuff like (edge) sharpening, blurring, etc. The segmentation is algorithms like voronoi and k-means clustering, superpixels, region growing, graph cuts, contour tracing, etc. Color assignment would assign colors to the segments, depending on the palette available, e.g.: Apply the palette color closest the average color of each segment. Then, postprocessing could do stuff like merging segments, smoothing segments, etc. Finally, rendering creates the paint-by-number template where the segments contain a number and each number corresponds with a color, or already is colored to see what the painted image would look like.

Maybe this can be of some inspiration:

- https://github.com/fogleman/primitive
- https://scikit-image.org/docs/0.25.x/auto_examples/segmentation/plot_segmentations.html

Perhaps it would be even better to segment while keeping the palette in mind, not just applying it afterwards. Maybe I could think of some error functions like similarity to original image, smoothness of the segments, size of the segments, etc. Then, I can try to find a way to minimize these. I believe that this would result in good paint-by-number images.

Additionally, it would be nice to be able to have the program select the best n colors from a palette. This way you could provide a lot of standard paint colors and then the program would tell you which one to buy. Perhaps this could be expanded by being able to provide multiple images and select the n best colors from the palette for such that not just one image is best, but all work for those same colors.
