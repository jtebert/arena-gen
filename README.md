# Arena Generator

*Programmatically generated environments for gridsim projects*

## Installation and setup

Create a Python3 virtual environment:

```shell
python3 -m venv venv
```

Activate the virtual environment (you can deactivate it with `deactivate`):

```shell
source venv/bin/activate
```

Install the dependencies:

```shell
pip install -r requirements.txt
```

## Running

With the virtual environment active, run:

```shell
python gen.py CONFIG_FILE.yml
```

where `CONFIG_FILE.yml` is a YAML configuration file containing the configuration parameters specified below. An example is provided as `demo_config.yml`.

## Parameters

- `output_dir` (str, optional):
  Directory where to save the generated images. If not specified, images will be placed in the current directory.
- `img_filename_prefix` (str, optional):
  Every image filename will start with this, followed by a 3-digit number (and `.png` suffix). If not specified, images will just be named as a number.
- `allow_overwrite` (bool, optional):
  Whether images with the same name will be overwritten. If true and an image exists, the script will quit instead of overwriting. Defaults to `false`

- `img_dim` (List[int, int]):
  Dimensions (width and height, in pixels) of the output images
- `num_imgs` (int):
  Number of images to generate and save
- `img_ind_offset` (int, optional):
  Offset of the numbering of saved images. This also determines the output image (see note below). Defaults to `0`.

- `frequency` (float):
  Base scale of the output noise (lower means smaller features)
- `octaves` (int):
  How many different frequencies (scales) of noise to add.
- `persistence` (float):
  Amplitude of each additional octave (relative to the preceding octave). This should be > 0 and < 1.
- `lacunarity` (float):
  Frequency (scale) of each layer (relative to the previous octave). This should be > 1.

## Notes

Because of the nature of Perlin and Simplex noise, they are deterministic. That means that if you provide the same parameters, you'll get the same image out. Generating different images is done by specifying an "offset" for the coordinates. That's done here with the `img_ind_offset` parameters. That means that images generated with the same parameters *and the same index*, will be the same, but you can generate new images by changing this offset.

Useful reading:

- [Making maps with noise functions](https://www.redblobgames.com/maps/terrain-from-noise/)