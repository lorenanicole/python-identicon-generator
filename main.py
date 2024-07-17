#!/usr/bin/env python3

import argparse
import hashlib
from PIL import Image, ImageDraw

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"


class Identicon:

    def __init__(self, input_str: str) -> None:
        self.md5hash_str: str = self._convert_string_to_sha_hash(input_str)

    def _convert_string_to_sha_hash(self, input_str: str) -> str:
        """
        Function that takes an input string and returns a md5 hexdigest string.

        :return: md5 hexdigest of an input string
        """
        if len(input_str) < 1:
            raise ValueError("Input string cannot be empty.")
        
        return hashlib.md5(input_str.encode('utf-8')).hexdigest()

    def _build_grid(self) -> list[list]:
        """
        Function that takes an input md5 hexdigest string and builds
        a list of lists using grid size to determine the size of the 
        grid. Each value within the list of lists contains a row of booleans
        that indicates if that given element will be filled with a color.

        :return: a list of lists representing a grid of the pixels to be drawn in a PIL Image
        """
        grid_size: int = 5
        grid: list = []
        for row_number in range(grid_size):
            row: list = list()
            for element_number in range(grid_size):
                element: int = row_number * grid_size + element_number + 6
                fill_element: bool = int(self.md5hash_str[element], base=16) % 2 == 0
                row.append(fill_element)
            grid.append(row)
        return grid

    def _generate_image_fill_color(self, md5hash_str: str) -> tuple:
        """
        Function that generates a R,G,B value to use to fill the PIL Image.

        :param md5hash_str: md5 hexdigest of an input string
        :return: a tuple of numbers representing the R,G.B value to fill the PIL Image
        """
        return tuple(int(md5hash_str[i:i+2], base=16) for i in range(0, 2*3, 2))

    def draw_image(self, filename: str=None) -> Image:
        """
        Function that generates a grid - a list of lists - indicating which pixels are to be filled
        and uses the md5hash_str to generate an image fill color. Function creates a PIL Image, drawing it,
        and saving it.

        :param filename: filename of PIL png image generated
        :return: None
        """

        fill_color: tuple = self._generate_image_fill_color(self.md5hash_str)
        grid: list[list] = self._build_grid()

        SQUARE: int = 50
        size: tuple = (5 * 50, 5 * 50)
        bg_color: tuple = (214,214,214)

        image: Image = Image.new("RGB", size, bg_color)
        draw: ImageDraw  = ImageDraw.Draw(image)

        # Makes the identicon symmetrical
        for i in range(5):
            grid[i][4] = grid[i][0]
            grid[i][3] = grid[i][1]

        for row in range(5):
            for element in range(5):
                # Boolean check to confirm 'True' to draw and fill the pixel in the iamge
                if grid[row][element]:
                    bounding_box: list[int] = [element * SQUARE, row * SQUARE, element * SQUARE + SQUARE, row * SQUARE + SQUARE]
                    # TODO: Should we use multiple fill colors? May need to draw multiple rectangles to obtain this
                    draw.rectangle(bounding_box, fill=fill_color)

        if not filename:
            filename: str = 'example'

        image.save(f'{filename}.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate an identicon with Python 3.", 
        usage="""Example: python main.py -s='931D387731bBbC988B31220' or add the optional -o flag to specify name of identicon 
        image generated such as python main.py -s='931D387731bBbC988B31220' -o='my_identicon.jpg'."""
    )

    def len_gt_zero(input_str: str):
        if len(input_str) > 0:
            return input_str
        raise argparse.ArgumentTypeError("Input string must have length greater than 0 in order to generate an identicon.")

    parser.add_argument(
        "-s",
        "--string",
        default="",
        type=str,
        required=True,
        help="An input string used to generate an identicon.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="",
        type=str,
        required=False,
        help="Name for output identicon image generated.",
    )
  
    args = parser.parse_args()

    identicon = Identicon(input_str=args.string)
    identicon.draw_image(filename=args.output)
