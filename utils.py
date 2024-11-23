import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
import alphabets
from typing import List, Tuple, Optional


def get_data(
    language: str, mode: str
) -> Tuple[Optional[str], Optional[ImageFont], Optional[str], Optional[float]]:
    if language not in alphabets.languages:
        print("Invalid language")
        return None, None, None, None

    lang_config = alphabets.languages[language]
    character = lang_config["chars"]
    font = ImageFont.truetype(lang_config["font_path"], lang_config["size"])
    sample_character = lang_config["sample_char"]
    scale = lang_config["scale"]

    char_list: str
    try:
        if len(character) > 1:
            char_list = character[mode]
        else:
            char_list = character["standard"]
    except Exception as e:
        print(f"Invalid mode for {language}: {e}")
        return None, None, None, None

    if language != "general":
        char_list = sort_chars(char_list, font, language)

    return char_list, font, sample_character, scale


def sort_chars(char_list: str, font: ImageFont, language: str) -> str:
    out_width, out_height = set_img_shape(len(char_list), language, font)
    out_image = set_out_img(out_width, out_height, char_list, font)
    zipped_lists = zip_brightness_to_char(out_image, char_list)
    chars_list = set_chars_list(len(char_list), zipped_lists)
    return chars_list


def set_img_shape(
    char_list_len: int, language: str, font: ImageFont
) -> Tuple[int, int]:
    draw = ImageDraw.Draw(Image.new("RGB", (100, 100)))
    test_char = alphabets.languages[language]["sample_char"]

    bbox = draw.textbbox((0, 0), test_char, font=font)
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    out_width = int(char_width * char_list_len)
    out_height = int(char_height)
    return out_width, out_height


def set_out_img(
    out_width: int, out_height: int, char_list: str, font: ImageFont
) -> Image:
    out_image = Image.new("L", (int(out_width), int(out_height)), 255)
    draw = ImageDraw.Draw(out_image)
    draw.text((0, 0), char_list, fill=0, font=font)
    cropped_image = ImageOps.invert(out_image).getbbox()
    out_image = out_image.crop(cropped_image)
    return out_image


def zip_brightness_to_char(out_image: Image, char_list: str) -> List[Tuple[float, str]]:
    brightness = [
        np.mean(np.array(out_image)[:, 10 * i : 10 * (i + 1)])
        for i in range(len(char_list))
    ]
    zipped_lists = list(zip(brightness, char_list))
    zipped_lists = sorted(zipped_lists)
    return zipped_lists


def set_chars_list(char_list_len: int, zipped_lists: List[Tuple[float, str]]) -> str:
    num_chars = min(char_list_len, 100)
    chars_list = ""
    counter = 0
    incremental_step = (zipped_lists[-1][0] - zipped_lists[0][0]) / num_chars
    current_value = zipped_lists[0][0]
    for value, char in zipped_lists:
        if value >= current_value:
            chars_list += char
            counter += 1
            current_value += incremental_step
        if counter == num_chars:
            break
    if chars_list[-1] != zipped_lists[-1][1]:
        chars_list += zipped_lists[-1][1]
    return chars_list


if __name__ == "__main__":
    result = get_data("chinese", "interesting")
    print(result)
