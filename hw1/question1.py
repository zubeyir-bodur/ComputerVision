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
    return np.array([[0 for _ in range(cols)] for _ in range(rows)])


def intersect(m, n):
    """
    Bitwise and operation (M AND N)
    for binary 2D matrices in the same size
    Assuming black is the foreground
    :param m: Matrix M
    :param n: Matrix N
    :return: M AND N, if the size of M is equal to N
        1x1 matrix if the length is different
    """
    if len(m) != len(n) or len(m[0]) != len(n[0]):
        return [[1]]
    out = zeros(len(m), len(m[0]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            out[i][j] = m[i][j] + n[i][j]
            if out[i][j] > 255:
                out[i][j] = 255
    return np.array(out)


def is_subset_of(m, n):
    """
    Checks if bitwise matrix M is a
    subset of N. That is, all 0's in M
    should be contained by N
    :param m: smaller set
    :param n: larger set
    :return: true if M is subset of N
    false if sizes are not equal
    """
    if len(m) != len(n) or len(m[0]) != len(n[0]):
        return False
    out = zeros(len(m), len(m[0]))
    # Multiply M and N bitwise
    for i in range(len(m)):
        for j in range(len(m[0])):
            out[i][j] = m[i][j] * n[i][j]
            if out[i][j] > 255:
                out[i][j] = 255
    # If M X N (bitwise) is equal to N, then
    # M is a subset of N
    for i in range(len(m)):
        for j in range(len(m[0])):
            if out[i][j] != n[i][j]:
                return False
    return True


def pad_len(str_el):
    """
    Get the pad lengths for computing morphological
    operations using a structuring element str_el
    :param str_el:
    :return: Tuple (a, a), (b, b):
        Where padding sizes are ((left, right), (top, bottom))
    and b is for the top and bottom.
    """
    a = math.floor(len(str_el) / 2)
    b = math.floor(len(str_el[0]) / 2)
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
    padded_a = np.pad(a, pad_len(b), mode='constant', constant_values=(255, 255))
    for i in range(rows):
        for j in range(cols):
            slice_of_padded_a = padded_a[i:i + len(b), j:j + len(b[0])]
            intersection = intersect(b, slice_of_padded_a)
            prod_intersection = np.prod(intersection)
            contains = prod_intersection == 0
            if contains:
                out[i][j] = 0
            else:
                out[i][j] = 255
    return np.array(out)


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
    padded_a = np.pad(a, pad_len(b), mode='constant', constant_values=(255, 255))
    for i in range(rows):
        for j in range(cols):
            slice_of_padded_a = padded_a[i:i + len(b), j:j + len(b[0])]
            if is_subset_of(b, slice_of_padded_a):
                out[i][j] = 0
            else:
                out[i][j] = 255
    return out


def opening(a, b):
    return dilation(erosion(a, b), b)


def closing(a, b):
    return erosion(dilation(a, b), b)


def main():
    # structuring element, all black, and a little bit large
    b = zeros(4, 4)

    # convert the png into python matrix
    image = Image.open("img/binary_image.png")
    a = np.array(image)

    """
    m = [[255, 255, 255, 255, 255, 255, 255, 255],
         [0, 0, 0, 0, 0, 0, 0, 255],
         [255, 255, 255, 0, 0, 0, 0, 255],
         [255, 255, 255, 0, 0, 0, 0, 255],
         [255, 255, 0, 0, 0, 0, 0, 255],
         [255, 255, 255, 0, 0, 0, 0, 255],
         [255, 255, 0, 0, 255, 255, 255, 255],
         [255, 255, 255, 255, 255, 255, 255, 255]]
    """
    # apply closing, opening, closing and then erosion:
    # referring from: https://www.researchgate.net/publication/267228362_A_new_Morphological_Approach_for_Noise_Removal_cum_Edge_Detection
    out = closing(opening(erosion(a, b), b), b)
    out2 = opening(erosion(out, b), b)
    out3 = dilation(dilation(out2, b), b)

    # display the output
    plt.style.use('grayscale')
    plt.imshow(out)
    plt.show()
    plt.imshow(out2)
    plt.show()
    plt.imshow(out3)
    plt.show()


if __name__ == '__main__':
    main()

