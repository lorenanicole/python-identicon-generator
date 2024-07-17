import subprocess
import os
import sys
from pathlib import Path
import time
import unittest


PROJECT_ROOT = Path(__file__).parent.parent.absolute()

from contextlib import contextmanager


@contextmanager
def redirect_stdout(new_out):
    # https://stackoverflow.com/questions/47066063/how-to-capture-python-subprocess-stdout-in-unittest
    old_stdout = os.dup(1)
    try:
        os.dup2(new_out, sys.stdout.fileno())
        yield
    finally:
        os.dup2(old_stdout, 1)
    

class TestHappyPath(unittest.TestCase):
    def test_fails_to_create_identicon_with_input_text_missing(self):
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.check_output(f'python3 {PROJECT_ROOT}/main.py', shell=True, stderr=subprocess.STDOUT).strip()
            self.assertIn(context.exception.message, "main.py: error: the following arguments are required: -s/--string")
    
    def test_creates_identicon_when_input_text_provided(self):
        pass


      # hash_str =convert_string_to_sha_hash("931D387731bBbC988B31220")
    # hash_str = convert_string_to_sha_hash("me@lorenamesa.com")
    # grid = build_grid(hash_str)
    # draw_image(grid, hash_str)

if __name__ == '__maipython -m unittest__':
    unittest.main()