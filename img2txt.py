"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""

import argparse
import cv2
import numpy as np
from typing import Tuple
from PIL import Image, ImageFont


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument(
        "--input", type=str, default="data/input.jpg", help="Path to input image"
    )
    parser.add_argument(
        "--output", type=str, default="data/output.txt", help="Path to output text file"
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="complex",
        choices=["simple", "complex"],
        help="10 or 70 different characters",
    )
    parser.add_argument(
        "--num_cols",
        type=int,
        default=150,
        help="number of character for output's width",
    )
    return parser.parse_args()


def draw(
    image_input: str, image_output: str, char_list: str, num_cols: int, scale: float
) -> None:
    image: np.ndarray = cv2.cvtColor(cv2.imread(image_input), cv2.COLOR_BGR2GRAY)
    cell_width, cell_height, num_rows, num_cols = get_shape_parameters(
        image, num_cols, scale
    )

    with open(image_output, "w") as output_file:
        for i in range(num_rows):
            chars_per_row: str = ""
            for j in range(num_cols):
                avg_gray: float = calc_avg_gray(image, cell_width, cell_height, i, j)
                ascii_char: str = get_char_by_gray(char_list, len(char_list), avg_gray)
                chars_per_row += ascii_char
            chars_per_row += "\n"
            output_file.write(chars_per_row)


def set_char_list(mode: str) -> str:
    if mode == "simple":
        CHAR_LIST = "@%#*+=-:. "
    else:
        CHAR_LIST = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        )
    return CHAR_LIST


def get_shape_parameters(
    image: np.ndarray, num_cols: int, scale: float
) -> Tuple[int, int, int, int]:
    height, width = image.shape
    cell_width: int = int(width / num_cols)
    cell_height: int = int(scale * cell_width)
    num_rows: int = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_rows = int(height / cell_height)
        num_cols = int(width / cell_width)
    return cell_width, cell_height, num_rows, num_cols


def calc_avg_gray(
    image: np.ndarray, cell_width: int, cell_height: int, row: int, col: int
) -> float:
    height, width = image.shape
    top: int = int(row * cell_height)
    bottom: int = min(int((row + 1) * cell_height), height)
    left: int = int(col * cell_width)
    right: int = min(int((col + 1) * cell_width), width)
    avg_gray: float = np.mean(image[top:bottom, left:right])
    return avg_gray


def get_char_by_gray(char_list: str, num_chars: int, gray: float) -> str:
    char_idx_temp: int = int(gray * num_chars / 255)
    char_idx_right_edge: int = num_chars - 1
    ascii_char: str = char_list[min(char_idx_temp, char_idx_right_edge)]
    return ascii_char


if __name__ == "__main__":
    opt = get_args()
    image_input: str = opt.input
    image_output: str = opt.output
    char_list: str = set_char_list(opt.mode)
    num_cols: int = opt.num_cols
    scale: float = 2

    draw(image_input, image_output, char_list, num_cols, scale)
