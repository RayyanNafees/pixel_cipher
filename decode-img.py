#!/usr/bin/python3

import argparse
import image_cipher as ic

description = """
This program coded message in img
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--orginal','-o',
                    required=True)

parser.add_argument('--coded', '-c',
                    required=True)

parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s 1.0',)

args = parser.parse_args()

path_orginal = args.orginal
path_coded = args.coded


decoded_msg = ic.decoded_img(path_orginal, path_coded)
print(decoded_msg)
