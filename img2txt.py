"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""

import cv2
import numpy as np
from utils import (
    get_args,
    get_data,
    get_char_by_color,
    get_shape_parameters,
    calc_avg_gray,
    get_partial_image,
)


def draw(
    image_input: str, image_output: str, num_cols: int, char_list: str, scale: float
) -> None:
    image: np.ndarray = cv2.cvtColor(cv2.imread(image_input), cv2.COLOR_BGR2GRAY)
    image_height, image_width = image.shape
    cell_width, cell_height, num_rows, num_cols = get_shape_parameters(
        image_height, image_width, num_cols, scale
    )

    with open(image_output, "w") as output_file:
        for i in range(num_rows):
            chars_per_row: str = ""
            for j in range(num_cols):
                partial_image = get_partial_image(image, cell_width, cell_height, i, j)
                avg_gray: float = calc_avg_gray(partial_image, num_cols)
                ascii_char: str = get_char_by_color(char_list, len(char_list), avg_gray)
                chars_per_row += ascii_char
            chars_per_row += "\n"
            output_file.write(chars_per_row)


if __name__ == "__main__":
    opt = get_args()
    image_input: str = opt.input
    image_output: str = opt.output
    language: str = opt.language
    mode: str = opt.mode
    num_cols: int = opt.num_cols
    scale: float = opt.scale

    try:
        char_list, _font, _sample_character, scale = get_data(language, mode)
    except ValueError:
        print("Error: Invalid language or mode.")
        exit(1)

    draw(image_input, image_output, num_cols, char_list, scale)
