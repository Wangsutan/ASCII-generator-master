"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""

import cv2
import numpy as np
from PIL import ImageDraw, ImageFont
from utils import (
    get_args,
    get_data,
    get_shape_parameters,
    get_char_shape,
    get_partial_image,
    get_char_by_color,
    get_out_image,
    calc_avg_gray,
    crop_image,
    set_background_code,
)


def draw(
    image_input: str,
    image_output: str,
    background_color: str,
    num_cols: int,
    char_list: str,
    font: ImageFont.FreeTypeFont,
    sample_character: str,
    scale: float,
) -> None:
    bg_code: int = set_background_code(backgroudnd_color)

    image: np.ndarray = cv2.cvtColor(cv2.imread(image_input), cv2.COLOR_BGR2GRAY)
    height, width = image.shape
    cell_width, cell_height, num_rows, num_cols = get_shape_parameters(
        height, width, num_cols, scale
    )

    char_width, char_height = get_char_shape(sample_character, font)
    out_image = get_out_image(
        char_width, char_height, num_cols, num_rows, scale, "L", bg_code
    )
    draw = ImageDraw.Draw(out_image)

    for i in range(num_rows):
        chars_per_row: str = ""
        for j in range(num_cols):
            partial_image: np.ndarray = get_partial_image(
                image, cell_width, cell_height, i, j
            )
            avg_gray: float = calc_avg_gray(partial_image, num_cols)
            ascii_char: str = get_char_by_color(char_list, len(char_list), avg_gray)
            chars_per_row += ascii_char
        chars_per_row += "\n"
        draw.text((0, i * char_height), chars_per_row, fill=255 - bg_code, font=font)

    out_image = crop_image(out_image, background_color)
    out_image.save(image_output)


if __name__ == "__main__":
    opt = get_args()
    image_input: str = opt.input
    image_output: str = opt.output
    backgroudnd_color: str = opt.background
    language: str = opt.language
    mode: str = opt.mode
    num_cols: int = opt.num_cols
    scale: float = opt.scale

    try:
        char_list, font, sample_character, scale = get_data(language, mode)
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
