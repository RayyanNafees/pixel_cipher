#!/usr/bin/python3
import json
import os
from PIL import Image
import numpy as np


class PixelCipher:

    def __init__(self):
        self.cfg = self.load_config()

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
        self.letter_to_number = self.cfg["letter_to_number"]
        self.pixels_array = self.coded_img(img, msg)
        self.save_img(self.pixels_to_img(self.pixels_array))

    def path_to_save_convert_image(self):
        path = os.path.join(self.cfg["path_to_save_coded_img"])
        if os.path.exists(path):
            path = os.path.join(path, self.cfg["name_convert_img"] + "." + self.cfg["extension"])
            return path
        else:
            raise FileExistsError

    def save_img(self, img):
        path = os.path.join(self.path_to_save_convert_image())
        img.save(path)

    def is_rgb_overload(self, pixel_first, pixel_second):
        if any([elem > 254 for elem in [*pixel_first, *pixel_second]]):
            return  True
        return False

    def coded_letter_to_bin(self, msg):
        for sign in msg:
            yield '{:06b}'.format(self.letter_to_number[sign])

    def coded_pixels(self, bin_letter, first_pixel, second_pixel):
        iteration = 0
        for bit in bin_letter:
            if bit == '1':
                if iteration > 2:
                    second_pixel[iteration-3] += 1
                else:
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
        self.number_to_letter = self.cfg["number_to_letter"]
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
    def __init__(self, cipher_message):
        self.msg = cipher_message
        self.code_table = self.get_code_table()

    def __str__(self):
        return 'message length: {}\nmessage content: "{}"'.format(len(self.msg), self.msg)

    def get_code_table(self):
        with open('config/decoding_table.json', 'r') as msg:
            cfg = json.load(msg)
        return cfg["letter_to_number"].keys()

    def in_coded_table(self, msg):
        for elem in msg:
            if elem not in self.code_table:
                raise Exception("Can't coded sign:", elem)
        return True
