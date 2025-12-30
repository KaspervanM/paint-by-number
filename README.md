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

But option 1 is preferred.

### Options

- `input_image` - Path to the image to convert
- `palette` - Path to a palette file (R,G,B per line)
- `--dir`, `-d` - Directory where the output will be saved (default: current working directory)
- `--output`, `-o` - Exact output file path (overrides --dir)
- `--algorithm`, `-a` - Algorithm to use (choices: nearest, floyd-steinberg)
- `--help`, `-h` - Show program help

## Notes

The project is a work in progress. So far, only two quantization algorithms have been implemented:

- nearest
- Floyd-Steinberg

I plan to implement segmentation algorithms to get one step closer to a true paint by number generator:

- Voronoi-based image segmentation
- K-means / clustering with spatial regularization
- Watershed segmentation
- Superpixels

And then apply the palette color closest the average color of each segment.

Maybe this can be of some inspiration:

- https://github.com/fogleman/primitive
- https://scikit-image.org/docs/0.25.x/auto_examples/segmentation/plot_segmentations.html

Perhaps it would be even better to segment while keeping the palette in mind, not just applying it afterwards. Maybe I could think of some error functions like similarity to original image, smootheness of the segments, size of the segments, etc. Then, I can try to find a way to minimize these. I believe that this would result in good paint-by-number images.
