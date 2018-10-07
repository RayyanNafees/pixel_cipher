#!/usr/bin/python3

import argparse
import image_cipher as ic
from image_cipher import Message

description = """
This program coded message in img
"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('--msg', '-m',
                    help='message to cipher only [a-z]',
                    type=str,
                    )

parser.add_argument('--msgpath',
                    '-mp',
                    help='message to cipher only [a-z]',
                    type=str,
                    )

parser.add_argument('--alphabetic', '-a',
                    nargs='?',
                    type=bool,
                    const=True,
                    help='message to cipher only [a-z]',
                   )

parser.add_argument('--path', '-p',
                    required=True)

parser.add_argument('--version', '-v',
                    action='version',
                    version='%(prog)s 1.0',)

args = parser.parse_args()

path = args.path

if args.msg:
    msg = Message(args.msg)
elif args.msgpath:
    msg = Message(args.msgpath)
    if args.alphabetic:
        msg.reduce_to_alphabetic(msg.read_path(args.msgpath))
else:
    msg = ''

if msg.is_only_alphabetic():
    msg.lowercase_msg()
    msg.rm_redundant_whitespace()
else:
    raise Exception("message must be only alphabetic, use --alphabetic flags")

print(msg.msg)

coded_img = ic.coded_img(path, msg.msg)

ic.array_to_image(coded_img)

