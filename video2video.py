"""
@author: Viet Nguyen <nhviet1009@gmail.com>
@author: Wang Sutan <wangsutan@163.com>
"""

import argparse
import cv2
import numpy as np
from utils import (
    get_data,
    set_background_code,
    get_shape_parameters,
    get_char_shape,
    get_out_image,
    get_partial_image,
    calc_avg_gray,
    get_char_by_color,
    crop_image,
)
from PIL import ImageFont, ImageDraw


def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument(
        "--input", type=str, default="data/input.mp4", help="Path to input video"
    )
    parser.add_argument(
        "--output", type=str, default="data/output.mp4", help="Path to output video"
    )
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument(
        "--background",
        type=str,
        default="white",
        choices=["black", "white"],
        help="background's color",
    )
    parser.add_argument(
        "--num_cols",
        type=int,
        default=100,
        help="number of character for output's width",
    )
    parser.add_argument("--scale", type=int, default=1, help="upsize output")
    parser.add_argument("--fps", type=int, default=0, help="frame per second")
    return parser.parse_args()


def draw(
    vedio_input: str,
    vedio_output: str,
    background_color: str,
    num_cols: int,
    char_list: str,
    font: ImageFont.FreeTypeFont,
    sample_character: str,
    scale: float,
    fps: int,
) -> None:
    bg_code: int = set_background_code(background_color)
    cap = cv2.VideoCapture(vedio_input)
    if fps == 0:
        fps = int(cap.get(cv2.CAP_PROP_FPS))

    while cap.isOpened():
        flag, frame = cap.read()
        if flag:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            break

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
                partial_image = get_partial_image(image, cell_width, cell_height, i, j)
                avg_gray: float = calc_avg_gray(partial_image, num_cols)
                ascii_char: str = get_char_by_color(char_list, len(char_list), avg_gray)
                chars_per_row += ascii_char
            chars_per_row += "\n"
            draw.text(
                (0, i * char_height), chars_per_row, fill=255 - bg_code, font=font
            )

        out_image = crop_image(out_image, background_color)
        out_image = cv2.cvtColor(np.array(out_image), cv2.COLOR_GRAY2BGR)
        out_image = np.array(out_image)

        out: cv2.VideoWriter
        try:
            out
        except NameError:
            out = cv2.VideoWriter(
                vedio_output,
                cv2.VideoWriter.fourcc(*"MJPG"),
                fps,
                ((out_image.shape[1], out_image.shape[0])),
            )
        out.write(out_image)
    cap.release()
    out.release()


if __name__ == "__main__":
    opt = get_args()
    vedio_input: str = opt.input
    vedio_output: str = opt.output
    backgroudnd_color: str = opt.background
    language: str = opt.language
    mode: str = opt.mode
    num_cols: int = opt.num_cols
    scale: float = opt.scale
    fps: int = opt.fps

    try:
        char_list, font, sample_character, scale = get_data(language, mode)
    except ValueError:
        print("Error: Invalid language or mode.")
        exit(1)

    draw(
        vedio_input,
        vedio_output,
        backgroudnd_color,
        num_cols,
        char_list,
        font,
        sample_character,
        scale,
        fps,
    )
