from sklearn.neighbors import KNeighborsClassifier
from PIL import Image
import numpy as np
import json
import time
import sys
import argparse
import os
from datetime import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_output_file_name(path):
    head, tail = os.path.split(path)
    file_ = tail or os.path.basename(head)
    return '.'.join(file_.split('.')[:-1]) + f"_{str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))}.png"


def load_emojis_json(file="emojis_data/colors_emojis_mean_unicode.json"):
    """
        The emojis json files is an array of arrays;
        Each array has the format: [emoji image path, [RGB values]]
    """
    with open(file) as emoji_json_data:
        emojis = np.array(json.load(emoji_json_data), dtype=object)
    colors = []
    emojis_files = []
    unicode_emojis = []
    for pair in emojis:
        emojis_files.append(np.array(pair[0]))
        colors.append(np.array(pair[1]))
        unicode_emojis.append(np.array(pair[2]))

    return [np.array(x) for x in (colors, emojis_files, unicode_emojis)]


def mirror_images(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width,
                             max(im1.height, im2.height)))
    dst.paste((0, 0, 0), [0, 0, dst.size[0], dst.size[1]])
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def stack_emojis_horizontally(files):
    """
        opens emojis images and stack them horizontally, might consider keep the images loaded.
        :files: array of emoji image paths.
    """
    images = [Image.open(file).convert('RGBA') for file in files]
    images_combined = np.hstack((np.asarray(image) for image in images))
    # TODO: add black background
    return Image.fromarray(images_combined)


def stack_emojis_vertically(images):
    """
        :images: array of PIL.Image
    """
    images_combined = np.vstack((np.asarray(image) for image in images))
    return Image.fromarray(images_combined)


def scale_image(image, scale):
    scaled_size = np.round(np.array(image.size) / scale).astype(int)
    return np.array(image.resize(scaled_size, Image.BILINEAR))


def convert_to_imoji(knn, emojis, image, unicode_emojis=None, bg_color=None):
    shape = image.shape[:2]
    pixels = image.reshape(-1, 3)
    indices = knn.predict(pixels).astype(int)
    emojis_rows = emojis[indices].reshape(shape)
    unicode_emojis = unicode_emojis[indices].reshape(shape)

    output = '\n'.join(['\u2009'.join(line) for line in unicode_emojis])
    with open("output_emoji.txt", "w", encoding="utf-8") as f:
        f.write(output)

    output_image = None
    for emoji_row in emojis_rows:
        row = stack_emojis_horizontally(emoji_row)
        # If we have previous row/s, stack them vertically
        if output_image is not None:
            row = stack_emojis_vertically([output_image, row])
        output_image = row

    if bg_color is not None:
        bg_img = Image.new("RGBA", output_image.size, bg_color)
        bg_img.paste(output_image, (0, 0), output_image)
        output_image = bg_img
    return output_image


def start_imoji(input_file, output_file, scale, mirror=False, bg_color=None):
    colors, emojis, unicode_emojis = load_emojis_json()
    knn = KNeighborsClassifier(n_neighbors=1, algorithm="kd_tree")
    knn.fit(X=colors, y=np.arange(len(colors)))
    original_image = Image.open(input_file)
    scaled_image = scale_image(original_image, scale)
    emoji_image = convert_to_imoji(
        knn, emojis, scaled_image, unicode_emojis, bg_color)
    if mirror:
        mirrored = mirror_images(original_image, emoji_image)
        mirrored.save(f"output/{output_file}")
        return mirrored
    else:
        emoji_image.save(f"output/{output_file}")
        return emoji_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Turns images into emojis! IMOJIS!')
    parser.add_argument('-s', '--scale', type=int, help="Divides the original image size by that scale, \
        1 for the original size, affects performance a lot.", default=15)
    parser.add_argument(
        '-i', '--input', help="input image file name", required=True)
    parser.add_argument(
        '-m', '--mirror', help="Add the original image next to the imoji", action="store_true")
    parser.add_argument(
        '-o', '--open', help="Open the image as well as saving it.", action="store_true")
    parser.add_argument(
        '-bg', '--background', help="Color for background.", default=None, action="store")

    args = parser.parse_args()
    t = time.time()

    if not os.path.exists("output"):
        os.makedirs("output")

    output = start_imoji(args.input, get_output_file_name(
        args.input), args.scale, args.mirror, args.background)
    print(f"Run time: {time.time()-t}")
    if args.open:
        output.show()
