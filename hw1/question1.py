"""
  Computer Vision HW 1 - Question 1
"""
import math

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def zeros(rows, cols):
    """
    Create a matrix of zeros
    :param rows:
    :param cols:
    :return:
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]


def subset_of(m, n):
    """
    Checks if bitwise matrix M is a
    subset of N. That is, all 1's in M
    should be contained by N
    :param m: smaller set
    :param n: larger set
    :return: true if M is subset of N
    false if sizes are not equal
    """
    if len(m) != len(n) or len(m[0]) != len(n[0]):
        return False
    out = zeros(len(m), len(m[0]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            out[i][j] = m[i][j] * n[i][j]
    return True


def intersect(m, n):
    """
    Bitwise and operation (M AND N)
    for binary 2D matrices in the same size
    :param m: Matrix M
    :param n: Matrix N
    :return: M AND N, if the size of M is equal to N
        1x1 zero matrix if the length is different
    """
    if len(m) != len(n) or len(m[0]) != len(n[0]):
        return [[0]]
    out = zeros(len(m), len(m[0]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            out[i][j] = m[i][j] * n[i][j]
    return out


def pad_len(str_el):
    """
    Get the pad lengths for computing morphological
    operations using a structuring element str_el
    :param str_el:
    :return: Tuple (a, a), (b, b):
        Where padding sizes are ((left, right), (top, bottom))
    and b is for the top and bottom.
    """
    a = math.ceil(len(str_el) / 2)
    b = math.ceil(len(str_el[0]) / 2)
    return (a, a), (b, b)


def dilation(a, b):
    """
    Dilation implementation according to the
    First definition of dilation operation
    :param a:  A, input image
    :param b: B, structuring element, can be any size
    :return: A (+) B, where the output has the same size as A
    """
    rows = len(a)
    cols = len(a[0])
    out = zeros(rows, cols)
    padded_a = np.pad(a, pad_len(b), mode='constant', constant_values=(0, 0))
    for i in range(rows):
        for j in range(cols):
            slice_of_padded_a = padded_a[i:i + len(b), j:j + len(b[0])]
            intersection = intersect(b, slice_of_padded_a)
            sum_intersection = np.sum(intersection)
            contains = sum_intersection > 0
            if contains:
                out[i][j] = 1
    return out


def erosion(a, b):
    """
    Erosion implementation according to the
    first definition of erosion operation
    :param a:  A, input image
    :param b: B, structuring element, can be any size
    :return: A (-) B, where the output has the same size as A
    """
    rows = len(a)
    cols = len(a[0])
    out = zeros(rows, cols)
    padded_a = np.pad(a, pad_len(b), mode='constant', constant_values=(0, 0))
    for i in range(rows):
        for j in range(cols):
            slice_of_padded_a = padded_a[i:i + len(b), j:j + len(b[0])]
            if subset_of(b, slice_of_padded_a):
                out[i][j] = 1
    return out


def opening(a, b):
    return dilation(erosion(a, b), b)


def closing(a, b):
    return erosion(dilation(a, b), b)


def main():
    # structuring element goes here
    b = [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]]

    # convert the png into python matrix
    image = Image.open("img/binary_image.png")
    a = np.array(image)

    # apply opening then closing
    out = closing(opening(a, b), b)

    # display the output
    plt.style.use('grayscale')
    plt.imshow(out)
    plt.show()


if __name__ == '__main__':
    main()
