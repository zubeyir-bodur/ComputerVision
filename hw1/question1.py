"""
  Computer Vision HW 1 - Question 1
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


# Given two matrices of equal size
# find the intersection of the two.
def intersect(m, n):
    """
    Bitwise and operation (M AND N)
    for binary 2D matrices in the same size
    :param m: Matrix M
    :param n: Matrix N
    :return: M AND N, if the size of M is equal to N
        1x1 zero matrix if the length is different
    """
    # return a 1x1 zero matrix for different length
    if len(m) != len(n) or len(m[0]) != len(n[0]):
        return [[0]]
    out = [[0 for _ in range(len(m[0]))] for _ in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m[0])):
            out[i][j] = m[i][j] * n[i][j]
    return out


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
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            slice_of_a = [[0 for _ in range(len(b[0]))] for _ in range(len(b))]

            intersection = intersect(b, slice_of_a)
            sum_intersection = np.sum(intersection)
            contains = sum_intersection > 0
            if contains:
                out[i][j] = 1
    return out
    flat_submatrices = np.array([
        a[i:(i + dilation_level), j:(j + dilation_level)]
        for i in range(pimg_shape[0] - h_reduce) for j in range(pimg_shape[1] - w_reduce)
    ])

    # replace the values either 255 or 0 by dilation condition
    image_dilate = np.array([255 if (i == structuring_kernel).any() else 0 for i in flat_submatrices])
    # obtain new matrix whose shape is equal to the original image size
    image_dilate = image_dilate.reshape(orig_shape)


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
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            intersects = False
            if intersects:
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
    # plt.imshow(out)
    plt.show()


if __name__ == '__main__':
    main()
