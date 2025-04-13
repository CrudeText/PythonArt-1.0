# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:24:16 2022

@author: willi
"""
##############################################################################
#    Art.py 
#    a library made to experiment with static abstract digital art
#    by William Arranz (CrudeText)
##############################################################################


########################
####  FROM SCRATCH  ####
########################

import math
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from collections import deque
from PIL import Image, ImageDraw

# Define the output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def maxlines(points):
    """
    Creates a mandala-like figure using all point-to-point connections
    from a regular polygon with the specified number of summits (points).
    """
    points += 1
    xlib = np.linspace(0, 2 * math.pi, points)
    xval = []
    yval = []
    for x in xlib:
        for y in xlib:
            xval.append(math.sin(x))
            yval.append(math.cos(x))
            xval.append(math.sin(y))
            yval.append(math.cos(y))

    plt.plot(xval, yval, linewidth=0.1)
    now = datetime.now().strftime("%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"mandala{now}.png")
    plt.savefig(filename, dpi=1000)
    plt.show()


def gradientImg(imgsizex, imgsizey):
    """
    Generates a smooth linear gradient image transitioning from black to yellow.
    The gradient moves horizontally and vertically across the canvas.
    """
    img = Image.new('RGB', (imgsizex, imgsizey))
    colorx = np.linspace(0, 256, imgsizex)
    colory = np.linspace(0, 256, imgsizey)
    for x, xc in enumerate(colorx):
        for y, yc in enumerate(colory):
            img.putpixel((x, y), (int(xc - 1), int(yc - 1), 0))
    img.show()


def randGradient(sizex=1920, sizey=1080, columnsize=10, increment=1,
                 darkvariation=10, lightvariation=10, vartotal=100,
                 R=127, G=127, B=127, randstart=False, randvariation=0,
                 save=False, customname="Jesus"):
    """
    Creates vertical color columns with randomly shifting shades.
    Each column starts from a base RGB and evolves with random variation.
    """
    img = Image.new('RGB', (sizex, sizey))
    columns = int(sizex / columnsize)
    percentageincr = 100 / columns
    percentage = 0
    for x in range(columns):
        print("Progress:", round(percentage, 2), "%")
        percentage += percentageincr
        if not randstart:
            Red, Green, Blue = R, G, B
        else:
            Red = np.random.randint(0, 256)
            Green = np.random.randint(0, 256)
            Blue = np.random.randint(0, 256)
        for z in range(sizey):
            if randvariation:
                darkvariation += np.random.randint(-randvariation, randvariation)
                lightvariation += np.random.randint(-randvariation, randvariation)
            randR = np.random.randint(0, vartotal)
            randG = np.random.randint(0, vartotal)
            randB = np.random.randint(0, vartotal)
            if randR < darkvariation: Red -= increment
            if randR > (vartotal - lightvariation): Red += increment
            if randG < darkvariation: Green -= increment
            if randG > (vartotal - lightvariation): Green += increment
            if randB < darkvariation: Blue -= increment
            if randB > (vartotal - lightvariation): Blue += increment
            for y in range(x * columnsize, (x + 1) * columnsize):
                img.putpixel((y, z), (Red, Green, Blue))

    now = datetime.now().strftime("%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"colorcolumn{now}.png")
    if save:
        if customname != "Jesus":
            img.save(os.path.join(OUTPUT_DIR, f"{customname}.png"))
        else:
            img.save(filename)
    else:
        return img


def SunRay(linenumber=30, ringnumber=1, imgsize=1000, shift=5, R=255, G=0, B=0,
           linethickness=5, inRatio=0.3, outRatio=1):
    """
    Draws symmetrical rays between two concentric rings of points.
    One ring is rotated with respect to the other to create a mandala-like pattern.
    """
    img = Image.new('RGB', (imgsize, imgsize))
    maxrad = imgsize * 0.9
    mid = imgsize // 2
    for _ in range(ringnumber):
        inside = np.linspace(0, 2 * math.pi, linenumber)
        outside = deque(np.linspace(0, 2 * math.pi, linenumber))
        outside.rotate(shift)
        outside = list(outside)
        img1 = ImageDraw.Draw(img)
        for a, b in zip(inside, outside):
            x1 = math.cos(a) * (maxrad * outRatio) + mid
            y1 = math.sin(a) * (maxrad * outRatio) + mid
            x2 = math.cos(b) * (maxrad * inRatio) + mid
            y2 = math.sin(b) * (maxrad * inRatio) + mid
            img1.line([(x1, y1), (x2, y2)], (R, G, B), linethickness)
    return img


def randSun(linenumber=2000, imgsize=10000, shift=5, R=255, G=0, B=0,
            linethickness=1, inRatio=0.3, outRatio=1, maxvarout=300, maxvarin=300):
    """
    Same as SunRay but introduces randomness to line ends and starts,
    and assigns random colors for each line.
    """
    img = Image.new('RGB', (imgsize, imgsize))
    maxrad = imgsize * 0.9
    mid = imgsize // 2
    inside = np.linspace(0, 2 * math.pi, linenumber)
    outside = deque(np.linspace(0, 2 * math.pi, linenumber))
    outside.rotate(shift)
    outside = list(outside)
    img1 = ImageDraw.Draw(img)
    for i in range(linenumber):
        randout = np.random.randint(-maxvarout, maxvarout)
        randin = np.random.randint(-maxvarin, maxvarin)
        a = outside[(i + randout) % linenumber]
        b = inside[(i + randin) % linenumber]
        x1 = math.cos(a) * (maxrad * outRatio) + mid
        y1 = math.sin(a) * (maxrad * outRatio) + mid
        x2 = math.cos(b) * (maxrad * inRatio) + mid
        y2 = math.sin(b) * (maxrad * inRatio) + mid
        color = (R, G, B)
        img1.line([(x1, y1), (x2, y2)], color, linethickness)
    return img


def PicMosaic(path, squaresize=10):
    """
    Transforms an image into a mosaic composed of square blocks.
    Each block is filled with the average color of its pixels.
    """
    img = Image.open(path, 'r')
    width, height = img.size
    width -= width % squaresize
    height -= height % squaresize
    img = img.crop((0, 0, width, height))
    pix = np.array(img)
    newimg = Image.new('RGB', (width, height))
    for col in range(0, width, squaresize):
        for lin in range(0, height, squaresize):
            block = pix[lin:lin + squaresize, col:col + squaresize]
            avg_color = tuple(np.mean(block.reshape(-1, 3), axis=0).astype(int))
            for y in range(col, col + squaresize):
                for x in range(lin, lin + squaresize):
                    newimg.putpixel((y, x), avg_color)
    img.close()
    return newimg
