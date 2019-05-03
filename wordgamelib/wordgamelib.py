#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import random
import platform

random.seed(time.time())
PLATFORM = platform.system().upper()

CONSONANTS = 'BCDFGHJKLMNPQRSTVWXYZ'
VOWELS = 'AEIOUÄÖÜ'

def clear_screen():
    if PLATFORM == 'NT':
        # Call 'CLS' on Windows
        os.system('cls')
    else:
        # Call 'CLEAR' on OSX and Linux
        os.system('clear')


def get_random_word(words):
    return unicode(random.choice(words).strip().decode('utf-8'))


def read_text_file(filename):
    try:
        with open(filename, 'r') as txtFile:
            # Read lines, use the ones that don't start with "#"
            txtLines = [line for line in txtFile.readlines() if line[0] != '#']
    except:
        sys.exit('Could not load ' + filename + '!')
    return txtLines
