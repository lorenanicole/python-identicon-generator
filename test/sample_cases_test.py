#!/usr/bin/env python3

from os import remove
from pathlib import Path
from PIL import Image, PngImagePlugin
import subprocess
import unittest

from src.main import Identicon

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    

class TestUI(unittest.TestCase):
    def test_ui_fails_to_create_identicon_with_input_string_missing(self):
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.check_output(f"python3 {PROJECT_ROOT}/src/main.py", shell=True, stderr=subprocess.STDOUT).strip()
        self.assertIn("main.py: error: the following arguments are required: -s/--string", context.exception.output.decode('utf-8'))
    
    def test_ui_fails_to_create_identicon_with_dimensions_lt_1(self):
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.check_output(f"python3 {PROJECT_ROOT}/src/main.py -d 0", shell=True, stderr=subprocess.STDOUT).strip()
        self.assertIn("main.py: error: argument -d/--dimensions: Input square dimension (same height and width) must be greater than 1.", context.exception.output.decode('utf-8'))


class TestHappyPath(unittest.TestCase):
    def test_successfully_creates_identicon(self):
        identicon = Identicon("931D387731bBbC988B31220")
        identicon.render(filename="output")
        generated_image = Image.open(f"{PROJECT_ROOT}/output.png", mode="r")
        self.assertIsInstance(generated_image, PngImagePlugin.PngImageFile)
        remove(f"{PROJECT_ROOT}/output.png")
    
    def test_successfully_creates_same_identicon_for_same_input_strings(self):
        # Make 1st identicon 
        identicon_john_1 = Identicon("john")
        identicon_john_1.render(filename="john1")
        # Make 2nd identicon
        identicon_john_2 = Identicon("john")
        identicon_john_2.render(filename="john2")

        # Assertions
        generated_john_1 = Image.open(f"{PROJECT_ROOT}/john1.png", mode="r")
        self.assertIsInstance(generated_john_1, PngImagePlugin.PngImageFile)

        generated_john_2 = Image.open(f"{PROJECT_ROOT}/john2.png", mode="r")
        self.assertIsInstance(generated_john_2, PngImagePlugin.PngImageFile)

        self.assertEqual(generated_john_1, generated_john_2)

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john1.png")
        remove(f"{PROJECT_ROOT}/john2.png")
    
    def test_does_not_create_same_identicon_for_different_input_strings(self):
        # Make 1st identicon 
        identicon_john = Identicon("john")
        identicon_john.render(filename="john")
        # Make 2nd identicon
        identicon_john_2 = Identicon("jane")
        identicon_john_2.render(filename="jane")

        # Assertions
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)

        generated_jane = Image.open(f"{PROJECT_ROOT}/jane.png", mode="r")
        self.assertIsInstance(generated_jane, PngImagePlugin.PngImageFile)

        self.assertNotEqual(generated_john, generated_jane)

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")
        remove(f"{PROJECT_ROOT}/jane.png")
    
    def test_successfully_resizes_identicon_gt_default_when_dimensions_provided(self):
        identicon_john = Identicon("john")
        identicon_john.render(filename="john", dimensions=450)

        # Assertions
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)
        self.assertEqual(generated_john.size, (450, 450))

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")

    def test_successfully_resizes_identicon_lt_default_when_dimensions_provided(self):
        identicon_john = Identicon("john")
        identicon_john.render(filename="john", dimensions=150)

        # Assertions
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)
        self.assertEqual(generated_john.size, (150, 150))

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")

if __name__ == "__main__":
    unittest.main()