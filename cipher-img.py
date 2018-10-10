#!/usr/bin/python3

import argparse
from pixel_cipher import Message, CodePixel

description = """
This program cipher message in pixels img.
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--cipher-message', '-c',
                    help='message to cipher only with coded table',
                    required=True,
                    )

parser.add_argument('--img-path', '-p',
                    required=True,
                    )

parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s 1.0',
                    )

args = parser.parse_args()

img_path = args.img_path
message = Message(args.cipher_message)

message.in_coded_table(message.msg)


cipher = CodePixel(img_path, message.msg)


