import os
import sys

import noise
import numpy as np
from PIL import Image
import yaml


def main(config_file):
    # Parameters
    with open(config_file) as file:
        PARAMS = yaml.load(file, Loader=yaml.FullLoader)

    # Make output directory
    output_dir = PARAMS.get('output_dir', '')
    img_filename_prefix = PARAMS.get('img_filename_prefix', '')
    allow_overwrite = PARAMS.get('allow_overwrite', False)
    os.makedirs(output_dir, exist_ok=True)

    img_dims = PARAMS['img_dim']
    num_imgs = PARAMS['num_imgs']
    img_ind_offset = PARAMS.get('img_ind_offset', 0)

    frequency = PARAMS['frequency']  # (scale)
    octaves = PARAMS['octaves']
    persistence = PARAMS['persistence']  # how amplitude changes/scales over octaves
    lacunarity = PARAMS['lacunarity']  # how frequency changes/scales over octaves

    make_valleys = PARAMS.get('make_valleys', False)

    worlds = []
    for img_ind in range(img_ind_offset, num_imgs+img_ind_offset):
        world = np.zeros(img_dims)
        for x in range(img_dims[0]):
            for y in range(img_dims[1]):
                tmp_noise = noise.pnoise2(
                    x / frequency,  # x
                    y / frequency,  # y
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=img_dims[0],
                    repeaty=img_dims[1],
                    base=img_ind)
                if make_valleys:
                    abs_noise = noise.pnoise2(
                        x / frequency,  # x
                        y / frequency,  # y
                        octaves=1,
                        persistence=persistence,
                        lacunarity=lacunarity,
                        repeatx=img_dims[0],
                        repeaty=img_dims[1],
                        base=img_ind)
                    if octaves > 1:
                        other_noise = noise.pnoise2(
                            x / (frequency*persistence),  # x
                            y / (frequency*persistence),  # y
                            octaves=octaves-1,
                            persistence=persistence,
                            lacunarity=lacunarity,
                            repeatx=img_dims[0],
                            repeaty=img_dims[1],
                            base=img_ind)
                    else:
                        other_noise = 0
                    world[x, y] = abs(abs_noise)+other_noise
                else:
                    world[x, y] = tmp_noise
        worlds.append(world)

        print(world.min(), world.max())

    # Rescale to fit in [0, 255]
    range_in = [min([w.min() for w in worlds]),
                max([w.max() for w in worlds])]
    range_out = [0, 255]

    for ind, world in enumerate(worlds):
        img_ind = ind + img_ind_offset
        world_scaled = (world-range_in[0]) * (range_out[1]-range_out[0]) / \
            (range_in[1]-range_in[0]) + \
            range_out[0]
        world_scaled = np.uint8(world_scaled)
        # Save image to file
        output_file = os.path.join(output_dir, img_filename_prefix+str(img_ind).zfill(3)+'.png')
        if not allow_overwrite and os.path.exists(output_file):
            # Overwriting isn't allowed, but file already exists
            raise IOError(f'File "{output_file}" exists, but overwriting is not allowed.')
        print(output_file)
        img = Image.fromarray(world_scaled, 'L')
        img.save(output_file)


if __name__ == '__main__':
    try:
        yaml_params = sys.argv[1]
    except IndexError:
        # No yaml file specified
        print('ERROR: Give me a YAML file for your parameters!')
        exit(1)
    main(yaml_params)
