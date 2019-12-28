#!/usr/bin/env python3

# System imports
import os
import random
import subprocess
import tempfile

# Local imports
from bing_image_search import *


class DangerousGenerator:
    BACKGROUND = 'dangerous.png'
    BACKGROUND_WIDTH = 768
    BACKGROUND_HEIGHT = 505
    RESIZE_MAX = 150

    def __init__(self, bing_api_key):
        self._debug = False
        self._bing_api_key = bing_api_key
        self._error_string = 'Unknown Error'
        self.word = ''
        self.image_file = ''

    def set_debug(self, debug):
        self._debug = debug

    def generate_random(self):
        self.word = ''
        self.image_file = ''
        for retry in range(0, 5):
            word = DangerousGenerator.get_word('noun-10K.txt')
            if self.generate_from_word(word):
                self.word = word
                return True
        self._error_string = 'Too many retries'
        return False

    def generate_from_word(self, word):
        search = BingImageSearch(self._bing_api_key)
        url = search.get_image_url(search_term=word, min_height=200, only_transparent=True)
        if len(url) == 0:
            return False
        if self._debug:
            print("IMAGE URL: %s" % url)
        content = BingImageSearch.get_image_bytes_for_url(url)
        if len(content) == 0:
            return False
        item_filename = tempfile.mkstemp(suffix='.png')[1]
        if self._debug:
            print("IMAGE BEFORE RESIZE: %s" % item_filename)
        with open(item_filename, 'wb') as f:
            f.write(content)
        resized_item_filename = tempfile.mkstemp(suffix='.png')[1]
        self.do_resize(item_filename, resized_item_filename, DangerousGenerator.RESIZE_MAX)
        if not self._debug:
            os.remove(item_filename)
        if self._debug:
            print("IMAGE AFTER RESIZE: %s" % resized_item_filename)
        width, height = self.get_dimensions(resized_item_filename)
        if self._debug:
            print("Image dimensions are %dx%d" % (width, height))
        x_offset = DangerousGenerator.BACKGROUND_WIDTH / 2 - width / 2
        y_offset = DangerousGenerator.BACKGROUND_HEIGHT - height - 100
        output_filename = tempfile.mkstemp(suffix='.png')[1]
        if self._debug:
            print("OUTPUT IMAGE: %s" % output_filename)
        command = "composite -geometry +%d+%d \"%s\" \"%s\" \"%s\"" % (
            x_offset, y_offset,
            resized_item_filename,
            DangerousGenerator.BACKGROUND,
            output_filename
        )
        if self._debug:
            print(command)
        subprocess.check_output(command, shell=True)
        if not self._debug:
            os.remove(resized_item_filename)
        if not os.path.isfile(output_filename):
            return False
        if os.stat(output_filename).st_size <= 0:
            return False
        self.image_file = output_filename
        return True

    def get_image_mime_type(self):
        return 'image/png'

    def get_noun(self):
        return self.word

    def get_image_path(self):
        return self.image_file

    def get_error(self):
        return self._error_string

    def do_resize(self, input_filename, output_filename, max_size):
        command = "convert \"%s\" -resize %dx%d \"%s\"" % (input_filename, max_size, max_size, output_filename)
        if self._debug:
            print(command)
        subprocess.check_output(command, shell=True)

    def get_dimensions(self, image_filename):
        command = "convert \"%s\" -format \"%%wx%%h\" info:" % image_filename
        if self._debug:
            print(command)
        dimensions = subprocess.check_output(command, shell=True)
        dimensions = dimensions.decode('UTF-8')
        dimensions = str.split(dimensions, 'x')
        dimensions = [int(x) for x in dimensions]
        return dimensions

    @staticmethod
    def get_word(dictionary_filename):
        word = ''
        margin = 100 # Must be at least twice the size of a word in the password dictionary
        with open(dictionary_filename, 'r') as f:
            f.seek(0, 2)
            fileSize = f.tell() - margin

            for i in range(1, 1000):
                pointer = random.randint(0, fileSize - margin)
                f.seek(pointer)
                word = f.readline()  # probably does not start on a word boundry
                word = f.readline()[:-1]
                if len(word) >= 1:
                    break
        return word
