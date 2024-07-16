#!/usr/bin/env python3

import hashlib
import argparse

__author__ = "Lorena Mesa"
__email__ = "me@lorenamesa.com"


def convert_string_to_sha_hash(input_str: str): 
    try:
        input_str = input_str.encode('utf-8')
        md5hash = hashlib.md5(input_str).hexdigest()
        decimal_int = int(md5hash, 16)
        # Exclude the leading '0b' when converting to binary str
        binary_str = bin(decimal_int)[2:]

        r,g,b = tuple(binary_str[i:i+2] 
                    for i in range(0, 2*3, 2))

        print(r, g, b)
    except TypeError:
        raise TypeError("Cannot encode string before hashing.")
    

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
  
    convert_string_to_sha_hash("931D387731bBbC988B31220")