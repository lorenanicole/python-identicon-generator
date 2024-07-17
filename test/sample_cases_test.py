#!/usr/bin/env python3

from pathlib import Path
from PIL import Image
import subprocess
import unittest

from main import Identicon

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    

class TestUI(unittest.TestCase):
    def test_ui_fails_to_create_identicon_with_input_text_missing(self):
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.check_output(f"python3 {PROJECT_ROOT}/main.py", shell=True, stderr=subprocess.STDOUT).strip()
            self.assertIn(context.exception.message, "main.py: error: the following arguments are required: -s/--string")


class TestHappyPath(unittest.TestCase):
    def test_successfully_creates_identicon(self):
        identicon = Identicon("931D387731bBbC988B31220")
        identicon.draw_image(filename="output")
        image = Image.open(f"{PROJECT_ROOT}/output.png", mode="r")
        self.assertIsInstance(image, Image, "Image created is not of type PIL.Image")

      # hash_str =convert_string_to_sha_hash("931D387731bBbC988B31220")
    # hash_str = convert_string_to_sha_hash("me@lorenamesa.com")
    # grid = build_grid(hash_str)
    # draw_image(grid, hash_str)

if __name__ == '__maipython -m unittest__':
    unittest.main()