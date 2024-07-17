#!/usr/bin/env python3

import argparse
import hashlib
import io
from PIL import Image, ImageDraw
import time

from sweepai.logn.cache import file_cache

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"


class Identicon:

    def __init__(self) -> None:
        self.md5hash_str: str = None
        self.grid_size: int = 5
        self.square_size: int = 64
        self.identicon_size: tuple = (self.grid_size * self.square_size, self.grid_size * self.square_size)

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
        a list of lists using self.GRID_SIZE to determine the size of the 
        grid; with the default set to a 5X5 grid. 
        
        Each value within the list of lists contains a row of booleans
        that indicates if that given pizel will be filled with a color.

        :return: a list of lists representing a grid of the pixels to be 
                 drawn and filled in a PIL Image
        """
        grid: list = []
        for row_number in range(self.grid_size):
            row: list = list()
            for pixel in range(self.grid_size):
                current_pixel: int = row_number * self.grid_size + pixel + 6
                fill_element: bool = int(self.md5hash_str[current_pixel], base=16) % 2 == 0
                row.append(fill_element)
            grid.append(row)
        return grid

    def _generate_pixel_fill_color(self, md5hash_str: str) -> tuple:
        """
        Function that generates a R,G,B value to use to fill the PIL Image pixels.

        :param md5hash_str: md5 hexdigest of an input string
        :return: a tuple of numbers representing the R,G,B value to fill the PIL Image pixels
        """
        return tuple(int(md5hash_str[i:i+2], base=16) for i in range(0, 2*3, 2))

    @file_cache()
    def render(self, input_str: str, filename: str="identicon", dimensions: int=0) -> Image:
        """
        Function that generates a grid - a list of lists - indicating which pixels 
        are to be filled and uses the md5hash_str to generate an image fill color. 
        Function creates a PIL Image, drawing it, and saving it. By default a 320 
        pixel by 320 pixel identicon is rendered, if upon executing the code a 
        dimensions parameter is passed in the image will be resized.

        :param input_str: unique identifer input string used to generate identicon
        :param filename: filename of PIL png image generated
        :return: None
        """

        # Can uncomment to confirm the @file_cache is working
        # import time; time.sleep(5)

        self.md5hash_str = self._convert_string_to_sha_hash(input_str)
        fill_color: tuple = self._generate_pixel_fill_color(self.md5hash_str)
        grid: list[list] = self._build_grid()

        # Default to a 320X320, a recommended avtar size per social platforms like Instagram, 
        # pixel image where each shape filled within the identicon is of size 64 pixels
        background_color: tuple = (214,214,214)
        image: Image = Image.new("RGB", self.identicon_size, background_color)
        draw: ImageDraw  = ImageDraw.Draw(image)

        # Makes the identicon symmetrical by setting the right columns
        # values to the same as the left columns, minus the center column
        for i in range(self.grid_size):
            grid[i][self.grid_size - 1] = grid[i][0]
            grid[i][self.grid_size - 2] = grid[i][1]

        for row in range(self.grid_size):
            for pixel in range(self.grid_size):
                # Boolean check to confirm 'True' to draw and fill the pixel in the iamge
                if grid[row][pixel]:
                    shape_coords: list[int] = [
                        pixel * self.square_size, 
                        row * self.square_size, 
                        pixel * self.square_size + self.square_size, 
                        row * self.square_size + self.square_size
                    ]
                    draw.rectangle(shape_coords, fill=fill_color)
  
        if dimensions:
            # Possible resampling filters here: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize
            # BICUBIC and LANCZOS take longer to process than NEAREST, but the quality of the former is better.
            width_percent: float = (dimensions / float(image.size[0]))
            height: int = int((float(image.size[1]) * float(width_percent)))
            image = image.resize((dimensions, height), Image.Resampling.LANCZOS)

        image.save(f'{filename}.png')

        # Return a unique string with the input str value and the image bytes array
        # to allow a cache hit

        byteIO = io.BytesIO()
        image.save(byteIO, format='PNG')
        im_bytes = byteIO.getvalue()
        # import pdb; pdb.set_trace()
        return f'{input_str}_{im_bytes}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate an identicon with Python 3.", 
        usage="""Example: python main.py -s='931D387731bBbC988B31220' or add the optional -o flag to specify name of identicon 
        image generated such as python main.py -s='931D387731bBbC988B31220' -o='my_identicon.jpg'." Additionally can specify the
        square dimensions in pixels for the identicon such as python main.py -s='931D387731bBbC988B31220' -d 150."""
    )
    def len_gt_zero(input_str: str):
        if len(input_str) > 0:
            return input_str
        else:
            raise argparse.ArgumentTypeError("Outfile filename must have length greater than 0 in order to generate an identicon.")
    def dimensions_gt_zero(input_dimensions: str):
        if not input_dimensions.isdigit():
            raise argparse.ArgumentTypeError("Input square dimension (same height and width) must be a legal int value.")
        elif int(input_dimensions) >= 1:
            return int(input_dimensions)
        else:
            raise argparse.ArgumentTypeError("Input square dimension (same height and width) must be greater than 1.")
    parser.add_argument(
        "-s",
        "--string",
        type=str,
        required=True,
        help="An input string used to generate a squaer identicon.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=len_gt_zero,
        help="Name for output square identicon PNG image generated.",
        default='identicon'
    )
    parser.add_argument(
        "-d",
        "--dimensions",
        type=dimensions_gt_zero,
        help="Optional dimensionals parameter for outputing square identicon image generated."
    )
  
    args = parser.parse_args()

    # Add timer to confirm performance of code
    t0 = time.time()
    identicon = Identicon()
    result = identicon.render(input_str=args.string, filename=args.output, dimensions=args.dimensions)
    t1 = time.time()
    print(f"{t1-t0} seconds to render {args.output}.png is now available to download!")
