import argparse
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import alphabets
from typing import Dict, List, Tuple


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
    parser.add_argument("--scale", type=int, default=2, help="upsize output")
    return parser.parse_args()


def get_data(language: str, mode: str = "standard") -> Tuple[
    str,
    ImageFont.FreeTypeFont,
    str,
    float,
]:
    if language not in alphabets.languages:
        raise ValueError(f"Language {language} not supported")

    lang_config: Dict = alphabets.languages[language]
    font: ImageFont.FreeTypeFont = ImageFont.truetype(
        lang_config["font_path"], lang_config["size"]
    )
    sample_character: str = lang_config["sample_char"]
    scale: float = lang_config["scale"]
    char_list: str = get_chars(lang_config["chars"], language, mode)
    if language != "general":
        char_list = sort_chars_incremental(char_list, font, language)

    return char_list, font, sample_character, scale


def get_shape_parameters(
    height: int, width: int, num_cols: int, scale: float
) -> Tuple[int, int, int, int]:
    cell_width: int = int(width / num_cols)
    cell_height: int = int(scale * cell_width)
    num_rows: int = int(height / cell_height)

    is_too_narrow: bool = num_cols > width or num_rows > height
    if is_too_narrow:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_rows = int(height / cell_height)
        num_cols = int(width / cell_width)

    return cell_width, cell_height, num_rows, num_cols


def get_chars(chars_dict: Dict, language: str, mode: str = "standard"):
    try:
        if len(chars_dict) > 1:
            return chars_dict[mode]
        else:
            return chars_dict["standard"]
    except Exception as e:
        raise ValueError(f"Invalid mode for {language}: {e}")


def get_out_image(
    char_width: int,
    char_height: int,
    num_cols: int,
    num_rows: int,
    scale: float,
    mode: str,
    bg_code: int | Tuple[int, int, int],
):
    out_width: int = char_width * num_cols
    out_height: int = int(char_height * num_rows * scale)
    out_image = Image.new(mode, (out_width, out_height), bg_code)
    return out_image


def sort_chars_incremental(
    char_list: str, font: ImageFont.FreeTypeFont, language: str
) -> str:
    sample_char = alphabets.languages[language]["sample_char"]
    char_width, char_height = get_char_shape(sample_char, font)
    out_width = int(char_width * len(char_list))
    out_height = int(char_height)
    img_chars_line = set_img_chars_line(out_width, out_height, char_list, font)
    b_c_list = calc_char_brightness(img_chars_line, char_width, char_list)
    return set_chars_incremental(len(char_list), b_c_list)


def get_char_shape(sample_char: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
    bbox = draw.textbbox((0, 0), sample_char, font=font)
    char_width = int(bbox[2] - bbox[0])
    char_height = int(bbox[3] - bbox[1])
    return char_width, char_height


def set_img_chars_line(
    out_width: int,
    out_height: int,
    char_list: str,
    font: ImageFont.FreeTypeFont,
) -> Image.Image:
    """add all character in list to image"""
    out_image = Image.new("L", (out_width, out_height), 255)
    draw = ImageDraw.Draw(out_image)
    draw.text((0, 0), char_list, fill=0, font=font)
    return out_image.crop(ImageOps.invert(out_image).getbbox())


def calc_char_brightness(
    img_chars_line: Image.Image, char_width: int, char_list: str
) -> List[Tuple[float, str]]:
    brightness_list: List[float] = []
    for i in range(len(char_list)):
        char_edge_left: int = char_width * i
        char_edge_right: int = char_width * (i + 1)
        brightness = np.mean(
            np.array(img_chars_line)[:, char_edge_left:char_edge_right]
        )
        brightness_list.append(brightness)
    zipped_lists = list(zip(brightness_list, char_list))
    return sorted(zipped_lists)


def set_chars_incremental(
    char_num: int, brightness2char_list: List[Tuple[float, str]]
) -> str:
    char_num_max: int = 100
    num_chars_actual: int = min(char_num, char_num_max)

    b_max: float = brightness2char_list[-1][0]
    b_min: float = brightness2char_list[0][0]
    incremental_step: float = (b_max - b_min) / num_chars_actual

    chars_incremental: str = ""
    brightness_current: float = brightness2char_list[0][0]
    num_chars_current: int = 0
    for b, c in brightness2char_list:
        if b >= brightness_current:
            chars_incremental += c
            brightness_current += incremental_step
            num_chars_current += 1
        if num_chars_current == num_chars_actual:
            break

    last_char: str = brightness2char_list[-1][1]
    if chars_incremental[-1] != last_char:
        chars_incremental += last_char

    return chars_incremental


def get_partial_image(
    image: np.ndarray, cell_width: int, cell_height: int, row: int, col: int
) -> np.ndarray:
    image_height, image_width = image.shape[:2]
    top: int = int(row * cell_height)
    bottom: int = min(int((row + 1) * cell_height), image_height)
    left: int = int(col * cell_width)
    right: int = min(int((col + 1) * cell_width), image_width)

    if len(image.shape) == 3:
        return image[top:bottom, left:right, :]
    else:
        return image[top:bottom, left:right]


def get_char_by_color(char_list: str, num_chars: int, value: float) -> str:
    char_idx_temp: int = int(value * num_chars / 255)
    char_idx_right_edge: int = num_chars - 1
    ascii_char: str = char_list[min(char_idx_temp, char_idx_right_edge)]
    return ascii_char


def calc_avg_gray(image: np.ndarray, num_chars: int) -> float:
    return np.mean(image) / 255 * num_chars


def calc_avg_color(
    image: np.ndarray, cell_width: int, cell_height: int
) -> Tuple[int, int, int]:
    partial_avg_color = np.sum(np.sum(image, axis=0), axis=0) / (
        cell_width * cell_height
    )
    return tuple(partial_avg_color.astype(np.int32).tolist())


def crop_image(image: Image.Image, background_color: str) -> Image.Image:
    if background_color == "white":
        cropped_image = ImageOps.invert(image).getbbox()
    else:
        cropped_image = image.getbbox()
    return image.crop(cropped_image)


if __name__ == "__main__":
    try:
        print(get_data("chinese", "interesting"))
    except Exception as e:
        print(e)
