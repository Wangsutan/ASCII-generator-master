"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""

import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont
from utils import get_data
from img2txt import calc_avg_gray, get_char_by_gray, get_shape_parameters
from typing import Tuple


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image"
    )
    parser.add_argument(
        "--output", type=str, default="data/output.jpg", help="Path to output text file"
    )
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument(
        "--background",
        type=str,
        default="black",
        choices=["black", "white"],
        help="background's color",
    )
    parser.add_argument(
        "--num_cols",
        type=int,
        default=300,
        help="number of character for output's width",
    )
    return parser.parse_args()


def draw(
    image_input: str,
    image_output: str,
    backgroudnd_color: str,
    num_cols: int,
    char_list: str,
    font: ImageFont,
    sample_character: str,
    scale: float,
) -> None:
    bg_code: int = set_background_code(backgroudnd_color)

    image: np.ndarray = cv2.cvtColor(cv2.imread(image_input), cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width, cell_height, num_rows, num_cols = get_shape_parameters(
        image, num_cols, scale
    )

    char_width, char_height = get_char_shape(sample_character, font)
    out_width: int = char_width * num_cols
    out_height: int = int(scale * char_height * num_rows)
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    for i in range(num_rows):
        chars_per_row: str = ""
        for j in range(num_cols):
            avg_gray: float = calc_avg_gray(image, cell_width, cell_height, i, j)
            ascii_char: str = get_char_by_gray(char_list, len(char_list), avg_gray)
            chars_per_row += ascii_char
        chars_per_row += "\n"
        draw.text((0, i * char_height), chars_per_row, fill=255 - bg_code, font=font)

    if bg_code == 255:
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(image_output)


def set_background_code(background_color: str) -> int:
    return 255 if background_color == "white" else 0


def get_char_shape(sample_character: str, font: ImageFont) -> Tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
    bbox = draw.textbbox((0, 0), sample_character, font=font)
    char_width = int(bbox[2] - bbox[0])
    char_height = int(bbox[3] - bbox[1])
    return char_width, char_height


if __name__ == "__main__":
    opt = get_args()
    image_input: str = opt.input
    image_output: str = opt.output
    backgroudnd_color: str = opt.background
    language: str = opt.language
    mode: str = opt.mode
    num_cols: int = opt.num_cols

    try:
        char_list, font, sample_character, scale = get_data(language, mode)
        if any(v is None for v in [char_list, font, sample_character, scale]):
            raise ValueError
    except ValueError:
        print("Error: Invalid language or mode.")
        exit(1)

    draw(
        image_input,
        image_output,
        backgroudnd_color,
        num_cols,
        char_list,
        font,
        sample_character,
        scale,
    )
