#!/usr/bin/python3
from PIL import Image
import numpy as np
import os

letter_to_number = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'r': 17,
    's': 18,
    't': 19,
    'u': 20,
    'w': 21,
    'x': 22,
    'y': 23,
    'z': 24,
    'v': 25,
    ' ': 26,
    '*': 27,
}

number_to_letter = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h',
    9: 'i',
    10: 'j',
    11: 'k',
    12: 'l',
    13: 'm',
    14: 'n',
    15: 'o',
    16: 'p',
    17: 'r',
    18: 's',
    19: 't',
    20: 'u',
    21: 'w',
    22: 'x',
    23: 'y',
    24: 'z',
    25: 'v',
    26: ' ',
    27: '*',
}


def path_to_save_convert_image(root_path=""):

    if os.path.exists(root_path):
        path = os.path.join(root_path,"convert_" + os.path.basename(img_src))
        return path
    else:
        raise FileExistsError

def img_to_array(img_src):

    img = Image.open(img_src)
    array = np.array(img)
    return array

def array_to_image(img_array):
    img = Image.fromarray(img_array)
    img.save("convert.png")

def pair_pixels(row):
    return zip(row[0::2], row[1::2])

def is_rgb_overload(pixel_x, pixel_y):

    is_overload_rgb = False
    is_overload = lambda pixel :any([ elem > 254 for elem in pixel])

    if is_overload(pixel_x) or is_overload(pixel_y):
        is_overload_rgb = True
    return is_overload_rgb

def code_letter_to_bin(msg):
    for elem in msg:
        yield '{:06b}'.format(letter_to_number[elem])

def code_pixe(to_code, first_pixel, second_pixel):
    iteration = 0
    for elem in to_code:
        if elem == '1':
            if iteration > 2:
                second_pixel[iteration-3] += 1
            elif elem == '1':
                first_pixel[iteration] += 1
        iteration += 1

def decoded_pixel(pair_pixel, pair_coded_pixel):
    orginal = [*pair_pixel[0], *pair_pixel[1]]
    coded = [*pair_coded_pixel[0], *pair_coded_pixel[1]]
    code = ''
    for org, cod in zip(orginal,coded):
        code+=(str(cod-org))
    if int(code,2) in number_to_letter.keys():
        decoded_pixel = number_to_letter[(int(code,2))]
    else:
        decoded_pixel = ''
    return decoded_pixel


def coded_img(img_src, message):

    img_array = img_to_array(img_src)
    get_code_letter = iter(code_letter_to_bin(message))

    for row in img_array:
        for first_pixel, second_pixel in pair_pixels(row):
            if not is_rgb_overload(first_pixel, second_pixel):
                try:
                    to_code = next(get_code_letter)
                    code_pixe(to_code, first_pixel, second_pixel)
                except StopIteration:
                    print('end coding')
                    return img_array


class Message:
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'message length: {}\nmessage content: "{}"'.format(len(self.msg), self.msg)

    def read_path(self, path):
        with open(path, 'r') as msg:
            return msg

    def reduce_to_alphabetic(self, msg):
        reduce_msg = ''
        for row in msg:
            for word in row.split():
                for sign in word:
                    if self.iscodesign(sign):
                        reduce_msg += ''.join(sign)
                reduce_msg+=''.join(' ')
        self.msg = reduce_msg

    def lowercase_msg(self):
        self.msg = self.msg.lower()
        return self.msg

    def is_only_alphabetic(self):
        isalpha_or_space = lambda elem: True if (elem.isalpha() or elem == ' ') else False
        is_alphabetic = False
        if all([ isalpha_or_space(elem) for elem in self.msg]):
            is_alphabetic = True
        return is_alphabetic

    def rm_redundant_whitespace(self):
        self.msg = ' '.join(self.msg.split())
        return self.msg

    def iscodesign(self, word):
        if word in letter_to_number.keys():
            return True
        return False




def decoded_img(img_path, coded_img_path):

    img_array =  img_to_array(img_path)
    coded_img_array = img_to_array(coded_img_path)
    msg = ''

    for row, coded_row in  zip(img_array, coded_img_array):
        for pair_pixel, pair_pixel_coded in zip(pair_pixels(row), pair_pixels(coded_row)):
            msg += decoded_pixel(pair_pixel, pair_pixel_coded)
    return msg

