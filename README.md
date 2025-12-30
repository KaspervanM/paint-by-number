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

Dependencies (currently just Pillow) will be installed automatically.

## Running the CLI

You can run the tool in several ways:

### 1. Using the installed console command

After installing with `pip install -e .`:

```bash
pbn images/my_image.png palettes/my_palette.txt
```

### 2. Using the module

For development, you could use:

```python
python3 -m pbn.cli images/my_image.png palettes/my_palette.txt
```

But option 1 is recommended.

### Usage

```
usage: pbn [-h] [-p {no-preprocessing,floyd-steinberg}] [-s {grid-segmentation}] [-c {average-nearest}] [--dir DIR] [--output OUTPUT] input_image palette

Paint by Number: Convert images to a palette-based representation. The resulting image is in PPM format.

positional arguments:
  input_image           Path to the input image.
  palette               Path to palette file (R,G,B per line).

options:
  -h, --help            show this help message and exit
  -p, --preprocessing {no-preprocessing,floyd-steinberg}
                        Preprocessing algorithm (optional).
  -s, --segmentation {grid-segmentation}
                        Segmentation algorithm to split the image into regions.
  -c, --assignment {average-nearest}
                        Color assignment algorithm to map palette colors to segments.
  --dir, -d DIR         Directory to save the output image. Default: current directory.
  --output, -o OUTPUT   Exact output file path. Overrides --dir if provided.

Author: Kasper van Maasdam. Date: December 2025. Licence: GPL v3.0
```

## Notes

The project is a work in progress. So far, only two quantization algorithms have been implemented:

- nearest
- Floyd-Steinberg

I plan to implement segmentation algorithms to get one step closer to a true paint by number generator:

- Voronoi-based image segmentation
- K-means / clustering with spatial regularization
- Watershed segmentation
- Superpixels
- region growing
- graph cuts
- contour tracing

And then apply the palette color closest the average color of each segment.

Maybe this can be of some inspiration:

- https://github.com/fogleman/primitive
- https://scikit-image.org/docs/0.25.x/auto_examples/segmentation/plot_segmentations.html

Perhaps it would be even better to segment while keeping the palette in mind, not just applying it afterwards. Maybe I could think of some error functions like similarity to original image, smootheness of the segments, size of the segments, etc. Then, I can try to find a way to minimize these. I believe that this would result in good paint-by-number images.
