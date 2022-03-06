"""
  Computer Vision HW 1 - Question 4
"""
import math
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def conv2(x, h):
    """
    2D convolution from scratch
    :return: h conv x, equivalent to x * h from conv theory
    """
    rows_x = len(x)
    cols_x = len(x[0])
    rows_h = len(h)
    cols_h = len(h[0])
    rows_y = rows_x + rows_h - 1
    cols_y = cols_x + cols_h - 1
    y = [[0 for _ in range(cols_y)] for _ in range(rows_y)]
    for i in range(rows_y):
        for j in range(cols_y):
            for u in range(rows_h):
                for v in range(cols_h):
                    if (i - u > -1) and (i - u < rows_x) and (j - v > -1) and (j - v < cols_x):
                        y[i][j] += h[u][v] * x[i-u][j-v]
    return y


def mag(dx, dy):
    """
    Given the gradient vectors dx and dy
    compute the gradient magnitude
    :param dx:
    :param dy:
    :return:
    """
    rows = len(dx)
    cols = len(dx[0])
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    if rows != len(dy) or cols != len(dy[0]):
        return
    for i in range(rows):
        for j in range(cols):
            out[i][j] = math.sqrt(dx[i][j] ** 2 + dy[i][j] ** 2)
    return out


def main():
    """
    Convolve Sobel and Prewitt matrices
    to the edge image. Sum horizontal and vertical
    values for each image. Then output the edge images
    :return: Outputs a plot, with sobel edges on left
    prewitt edges on the right
    """
    sobel_vertical = [[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]]
    sobel_horizontal = [[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]]

    prewitt_vertical = [[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]]

    prewitt_horizontal = [[-1, -1, -1],
                          [0, 0, 0],
                          [1, 1, 1]]

    # convert the png into python matrix
    image = Image.open("img/filter.jpg")
    x = np.array(image)

    x_s_vertical = conv2(x, sobel_vertical)
    x_s_horizontal = conv2(x, sobel_horizontal)

    x_p_vertical = conv2(x, prewitt_vertical)
    x_p_horizontal = conv2(x, prewitt_horizontal)

    x_edges_s = mag(x_s_vertical, x_s_horizontal)
    x_edges_p = mag(x_p_vertical, x_p_horizontal)

    # display the output
    plt.style.use('grayscale')
    plt.imshow(x_edges_s)
    plt.show()
    plt.imshow(x_edges_p)
    plt.show()


if __name__ == "__main__":
    main()
