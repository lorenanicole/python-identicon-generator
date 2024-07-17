#!/usr/bin/env python3

import argparse
import hashlib
from PIL import Image, ImageDraw

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"


def convert_string_to_sha_hash(input_str: str) -> str:
    input_str = input_str.encode('utf-8')
    return hashlib.md5(input_str).hexdigest()

def build_grid(md5hash: str) -> list[list]:
    grid_size = 5
    grid = []
    for i in range(grid_size):
        row = list()
        for j in range(grid_size):
            c = i * grid_size + j + 6
            # List of lists with booleans
            # Make a filter indicating which pixels to fill
            b = int(md5hash[c], base=16) % 2 == 0
            row.append(b)
        grid.append(row)
    return grid

def generate_foreground_color(hash_str: str) -> tuple:
    return tuple(int(hash_str[i:i+2], base=16) for i in range(0, 2*3, 2))

def draw_image(grid: list[list], hash_str: str) -> Image:

    fill_color = generate_foreground_color(hash_str)

    SQUARE = 50
    size = (5 * 50, 5 * 50)
    bg_color  = (214,214,214)

    image = Image.new("RGB", size, bg_color)
    draw  = ImageDraw.Draw(image)

    # Makes the identicon symmetrical
    for i in range(5):
        grid[i][4] = grid[i][0]
        grid[i][3] = grid[i][1]

    for x in range(5):
        for y in range(5):
            if grid[x][y]:
                bounding_box = [y * SQUARE, x * SQUARE, y * SQUARE + SQUARE, x * SQUARE + SQUARE]
                # TODO: Should we use multiple fill colors? May need to draw multiple rectangles to obtain this
                draw.rectangle(bounding_box, fill=fill_color)

    image.show()
    # TODO: Customize with name if arg provided
    image.save("example.png")
    return image

if __name__ == '__main__':
    # usage = """
    # python identicon.py -text="hello world"
    # python identicon.py -text="Thy bones are marrowless, thy blood is cold."
    # python identicon.py -text="bill.gates@microsoft.com" -dir="path/to/folder"
    # """
    # parser = argparse.ArgumentParser(
    #     description="Generate an identicon with Python 3.", 
    #     usage="""Example: python main.py -s='931D387731bBbC988B31220' or add the optional -o flag to specify name of identicon 
    #     image generated such as python main.py -s='931D387731bBbC988B31220' -o='my_identicon.jpg'."""
    # )

    # def len_gt_zero(input_str: str):
    #     if len(input_str) > 0:
    #         return input_str
    #     raise argparse.ArgumentTypeError("Input string must have length greater than 0 in order to generate an identicon.")

    # parser.add_argument(
    #     "-s",
    #     "--string",
    #     default="",
    #     type=str,
    #     required=True,
    #     help="An input string used to generate an identicon.",
    # )
    # parser.add_argument(
    #     "-o",
    #     "--output",
    #     default="",
    #     type=str,
    #     required=False,
    #     help="Name for output identicon image generated.",
    # )
  
    # args = parser.parse_args()
  
    # hash_str =convert_string_to_sha_hash("931D387731bBbC988B31220")
    hash_str = convert_string_to_sha_hash("me@lorenamesa.com")
    grid = build_grid(hash_str)
    draw_image(grid, hash_str)