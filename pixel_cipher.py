#!/usr/bin/python3
from PIL import Image
import numpy as np
import os
import json

class PixelCipher:

    def __init__(self):
        self.CFG = self.load_config()

    def load_config(self):
        with open('config/decoding_table.json', 'r') as msg:
            cfg = json.load(msg)
        return cfg

    def img_to_pixels_array(self, img_path):
        if not os.path.exists(img_path):
            raise  FileExistsError
        img = Image.open(img_path)
        array = np.array(img)
        return array

    def pixels_to_img(self, pixels_array):
        img = Image.fromarray(pixels_array)
        return img

    def pair_pixels(self, row):
        return zip(row[0::2], row[1::2])


class CodePixel(PixelCipher):

    def __init__(self, img, msg):
        super().__init__()
        self.letter_to_number = self.CFG["letter_to_number"]
        self.pixels_array = self.coded_img(img, msg)
        self.save_img(self.pixels_to_img(self.pixels_array))

    def path_to_save_convert_image(self):
        path = os.path.join(self.CFG["path_to_save_coded_img"])
        if os.path.exists(path):
            path = os.path.join(path, self.CFG["name_convert_img"] + "." + self.CFG["extension"])
            return path
        else:
            raise FileExistsError

    def save_img(self, img):
        path = os.path.join(self.path_to_save_convert_image())
        img.save(path)

    def is_rgb_overload(self, pixel_first, pixel_second):
        overload = False
        is_overload = lambda pixel :any([ elem > 254 for elem in pixel])
        if is_overload(pixel_first) or is_overload(pixel_second):
            overload = True
        return overload

    def coded_letter_to_bin(self, msg):
        for elem in msg:
            yield '{:06b}'.format(self.letter_to_number[elem])

    def coded_pixels(self, bin_letter, first_pixel, second_pixel):
        iteration = 0
        for bit in bin_letter:
            if bit == '1':
                if iteration > 2:
                    second_pixel[iteration - 3] += 1
                elif bit == '1':
                    first_pixel[iteration] += 1
            iteration += 1

    def coded_img(self, img_path, msg):
        pixels_array = self.img_to_pixels_array(img_path)
        get_bin_letter = iter(self.coded_letter_to_bin(msg))
        for row in pixels_array:
            for first_pixel, second_pixel in self.pair_pixels(row):
                if not self.is_rgb_overload(first_pixel, second_pixel):
                    try:
                        self.coded_pixels(next(get_bin_letter), first_pixel, second_pixel)
                    except StopIteration:
                        return pixels_array



class DecodedPixel(PixelCipher):

    def __init__(self, img_orginal, img_coded):
        super().__init__()
        self.number_to_letter = self.CFG["number_to_letter"]
        self.decoded_msg = self.decoded_img(img_orginal, img_coded)


    def __str__(self):
        return self.decoded_msg

    def decoded_pixel(self, pair_pixel, pair_coded_pixel):
        original = [*pair_pixel[0], *pair_pixel[1]]
        coded = [*pair_coded_pixel[0], *pair_coded_pixel[1]]
        bin_code = ''
        for org, cod in zip(original, coded):
            bin_code += (str(cod - org))
        if str(int(bin_code, 2)) in self.number_to_letter.keys():
            decoded_pixel = self.number_to_letter[str((int(bin_code, 2)))]
        else:
            decoded_pixel = ''
        return decoded_pixel


    def decoded_img(self, img_path, coded_img_path):
        pixels_array = self.img_to_pixels_array(img_path)
        coded_img_array = self.img_to_pixels_array(coded_img_path)
        encrypted_msg = ''
        for row, coded_row in zip(pixels_array, coded_img_array):
            for pair_pixel, pair_pixel_coded in zip(self.pair_pixels(row), self.pair_pixels(coded_row)):
                encrypted_msg += self.decoded_pixel(pair_pixel, pair_pixel_coded)
        return encrypted_msg


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


CodePixel('/home/an/Pulpit/a.jpg', 'kkgk')
b = DecodedPixel("/home/an/Pulpit/a.jpg", "/home/an/PycharmProjects/pixel_cipher/convert.png")
print(b)