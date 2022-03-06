"""
  Computer Vision HW 1 - Question 2
"""
import math

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def grayscale(rgb):
    """
    Convert the 3D RGB numpy image into
    2D grayscale image
    the values range between 0 and 255, and decimal
    :return:
    """
    out = [[0.0 for _ in range(len(rgb[0]))] for _ in range(len(rgb))]
    for i in range(len(rgb)):
        for j in range(len(rgb[0])):
            if rgb[0].ndim == 3:
                out[i][j] = (int(rgb[i][j][0]) + int(rgb[i][j][1]) + int(rgb[i][j][2])) / 3
            elif rgb[0].ndim == 2:
                out[i][j] = int(rgb[i][j][0])
            else:
                out[i][j] = int(rgb[i][j])
    return out


def histogram(matrix):
    """
    np.histogram implementation from scratch
    Assuming that input is a 2D grayscale matrix,
    and the interval start, width and count params
    for this histogram is constant:
        width = 1
        start = 0
        count = 256
    :return: frequency array, hist
    """
    hist = [0 for _ in range(256)]
    d1 = np.array(matrix).flatten()
    for i in range(len(d1)):
        index = math.floor(d1[i])
        if (index > -1) and (index < 256):
            hist[index] += 1
    return hist


def compute(pil_image):
    """
    Given a grayscale pil image,
    displays a histogram for the image
    for a grayscale histogram
    :param pil_image: input image, 2D matrix
    :return:
    """
    # convert the 3D matrix into 2D grayscale
    np_array = np.array(pil_image)
    two_d = grayscale(np_array)
    # compute a histogram out of 1D image array
    left = [i for i in range(256)]
    width = [1 for _ in range(256)]
    hist = histogram(two_d)
    plt.style.use('grayscale')
    plt.bar(left, hist, align='edge', width=width)
    plt.show()


def main():

    # convert the png into python matrix
    image1 = Image.open("img/grayscale_1.jpg")
    image2 = Image.open("img/grayscale_2.jpg")
    image3 = Image.open("img/otsu_1.jpg")
    image4 = Image.open("img/otsu_2.png")
    compute(image1)
    compute(image2)
    compute(image3)
    compute(image4)


if __name__ == '__main__':
    main()
