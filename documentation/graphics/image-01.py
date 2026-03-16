#!/usr/bin/env python3
"""Instruments Serif specimen image 1: Weight waterfall (Instagram portrait)"""

from drawbot_skia.drawbot import *
from fontTools.ttLib import TTFont
from fontTools.misc.fixedTools import floatToFixedToStr
import argparse
import subprocess
import sys

# Constants (1080x1440 @2x for Instagram portrait 3:4)
WIDTH, HEIGHT, MARGIN, FRAMES = 1080 * 2, 1440 * 2, 120*2, 1
GRID_VIEW = False

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--output", metavar="PNG", help="where to write the PNG file")
args = parser.parse_args()

# Font path
FONT_PATH = "fonts/InstrumentsSerif[wght].ttf"


# Helper functions
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin
    outputSpan = outputMax - outputMin
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)


def grid():
    stroke(1, 0, 0)
    strokeWidth(2)
    fill(None)
    rect(MARGIN, MARGIN, WIDTH - MARGIN * 2, HEIGHT - MARGIN * 2)
    step = MARGIN / 2
    x = MARGIN
    while x <= WIDTH - MARGIN:
        line((x, MARGIN), (x, HEIGHT - MARGIN))
        x += step
    y = MARGIN
    while y <= HEIGHT - MARGIN:
        line((MARGIN, y), (WIDTH - MARGIN, y))
        y += step
    strokeWidth(4)
    line((WIDTH / 2, MARGIN), (WIDTH / 2, HEIGHT - MARGIN))
    line((MARGIN, HEIGHT / 2), (WIDTH - MARGIN, HEIGHT / 2))


def draw_background():
    newPage(WIDTH, HEIGHT)
    fill(0.05)
    rect(-2, -2, WIDTH + 2, HEIGHT + 2)
    if GRID_VIEW:
        grid()


def draw_main_text():
    fill(0.7)
    stroke(None)
    TEXT = "Instruments Serif"
    weights = [400, 456, 511, 567, 622, 678, 733, 789, 844, 900]
    font(FONT_PATH)
    fontSize(256+32)
    y_top = HEIGHT - MARGIN - 210
    y_bottom = MARGIN + 60
    step = MARGIN + 4
    for i, wght in enumerate(weights):
        y = y_top - (i * step)
        fontVariations(wght=wght)
        text(TEXT, (MARGIN-16, y))


# Main
if __name__ == "__main__":
    draw_background()
    draw_main_text()
    if args.output:
        saveImage(args.output)
        print(f"DrawBot: Saved {args.output}")
    else:
        saveImage("documentation/graphics/image-01.png")
        print("DrawBot: Saved documentation/graphics/image-01.png")
    print("DrawBot: Done")
