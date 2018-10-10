#!/usr/bin/python3

import argparse
from pixel_cipher import DecodedPixel

description = """
This program coded message in img
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--original-img','-o',
                    required=True)

parser.add_argument('--cipher-img', '-c',
                    required=True)

parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s 1.0',)

args = parser.parse_args()
decipher = DecodedPixel(args.original_img, args.cipher_img)
print(decipher)
