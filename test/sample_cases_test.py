#!/usr/bin/env python3

from os import remove
from pathlib import Path
import shutil
from PIL import Image, PngImagePlugin
import subprocess
import time
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
        identicon = Identicon()
        identicon.render(input_str="931D387731bBbC988B31220", filename="output")
        generated_image = Image.open(f"{PROJECT_ROOT}/output.png", mode="r")
        self.assertIsInstance(generated_image, PngImagePlugin.PngImageFile)

        # Cleanup
        remove(f"{PROJECT_ROOT}/output.png")
        shutil.rmtree("/tmp/file_cache")
    
    def test_successfully_creates_same_identicon_for_same_input_strings(self):
        # Make 1st identicon 
        identicon_john_1 = Identicon()
        identicon_john_1.render(input_str="john", filename="john1")
        # Make 2nd identicon
        identicon_john_2 = Identicon()
        identicon_john_2.render(input_str="john", filename="john2")

        # Assertions
        generated_john_1 = Image.open(f"{PROJECT_ROOT}/john1.png", mode="r")
        self.assertIsInstance(generated_john_1, PngImagePlugin.PngImageFile)

        generated_john_2 = Image.open(f"{PROJECT_ROOT}/john2.png", mode="r")
        self.assertIsInstance(generated_john_2, PngImagePlugin.PngImageFile)

        self.assertEqual(generated_john_1, generated_john_2)

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john1.png")
        remove(f"{PROJECT_ROOT}/john2.png")
        shutil.rmtree("/tmp/file_cache")
    
    def test_does_not_create_same_identicon_for_different_input_strings(self):
        # Make 1st identicon 
        identicon_john = Identicon()
        identicon_john.render(input_str="john", filename="john")
        # Make 2nd identicon
        identicon_john_2 = Identicon()
        identicon_john_2.render(input_str="jane", filename="jane")

        # Assertions
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)

        generated_jane = Image.open(f"{PROJECT_ROOT}/jane.png", mode="r")
        self.assertIsInstance(generated_jane, PngImagePlugin.PngImageFile)

        self.assertNotEqual(generated_john, generated_jane)

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")
        remove(f"{PROJECT_ROOT}/jane.png")
        shutil.rmtree("/tmp/file_cache")
    
    def test_successfully_resizes_identicon_gt_default_when_dimensions_provided(self):
        identicon_john = Identicon()
        identicon_john.render(input_str="john", filename="john", dimensions=450)

        # Assertions
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)
        self.assertEqual(generated_john.size, (450, 450))

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")
        shutil.rmtree("/tmp/file_cache")

    def test_successfully_resizes_identicon_lt_default_when_dimensions_provided(self):
        identicon_john = Identicon()
        identicon_john.render(input_str="john", filename="john", dimensions=150)

        # Assertions
        # import pdb; pdb.set_trace()
        generated_john = Image.open(f"{PROJECT_ROOT}/john.png", mode="r")
        self.assertIsInstance(generated_john, PngImagePlugin.PngImageFile)
        self.assertEqual(generated_john.size, (150, 150))

        # Cleanup 
        remove(f"{PROJECT_ROOT}/john.png")
        shutil.rmtree("/tmp/file_cache")

class TestFileCache(unittest.TestCase):
    def test_successfully_skips_cache_if_identicon_already_made(self):
        # Call first time to instantiante in the file cache
        t0 = time.time()
        identicon_johnny = Identicon()
        identicon_johnny.render(input_str="johnny", filename="johnny", dimensions=150)
        t1 = time.time()
        johnny_1_time = t1 - t0

        # Call second time to retrieve from the file cache
        t0 = time.time()
        identicon_johnny_2 = Identicon()
        identicon_johnny_2.render(input_str="johnny", filename="johnny", dimensions=150)
        t1 = time.time()
        johnny_2_time = t1 - t0

        # Assertions
        self.assertLess(johnny_2_time, johnny_1_time)

        # Cleanup 
        remove(f"{PROJECT_ROOT}/johnny.png")
        shutil.rmtree("/tmp/file_cache")

if __name__ == "__main__":
    unittest.main()