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
    get_partial_image,
    calc_avg_color,
    crop_image,
    get_char_by_color,
    set_background_codes,
)
from img2img import get_char_shape, get_out_image
from typing import Tuple


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
    bg_code: Tuple[int, int, int] = set_background_codes(backgroudnd_color)

    image: np.ndarray = cv2.cvtColor(
        cv2.imread(image_input, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB
    )
    image_height, image_width = image.shape[:2]
    cell_width, cell_height, num_rows, num_cols = get_shape_parameters(
        image_height, image_width, num_cols, scale
    )

    char_width, char_height = get_char_shape(sample_character, font)
    out_image = get_out_image(
        char_width, char_height, num_cols, num_rows, scale, "RGB", bg_code
    )
    draw = ImageDraw.Draw(out_image)

    for i in range(num_rows):
        for j in range(num_cols):
            partial_image: np.ndarray = get_partial_image(
                image, cell_width, cell_height, i, j
            )
            partial_avg_color: Tuple[int, int, int] = calc_avg_color(
                partial_image, cell_width, cell_height
            )
            char: str = get_char_by_color(
                char_list, len(char_list), float(np.mean(partial_avg_color))
            )
            draw.text(
                (j * char_width, i * char_height),
                char,
                fill=partial_avg_color,
                font=font,
            )

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
