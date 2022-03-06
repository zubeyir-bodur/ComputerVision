"""
  Computer Vision HW 1 - Question 3
"""
import math
import sys

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def otsu_threshold(matrix):
    """
    Currently works imperfect for transparent png images,
    as the method extracts the grayscale values of those images
    Does not work for RGB images

    Otsu Threshold from scratch:
    Separates background & foreground from an image

    For each t value
        partition the matrix into s1 and s2
        compute the weighted sum of variances of partitions
        add into the results array

    get the index of the minimum result, optimal value of t
    partition the matrix into s1 and s2 s.t.
        s1 and s2 have the same size as matrix
        for each pixel in matrix
            if pixel belongs to s1
                add pixel to s1
            else
                add pixel to s2

    Display the partitions
    end
    :return
    """
    # Find t
    results = []
    if matrix.ndim == 3:
        matrix = matrix[:, :, 0]
    for t in range(0, 256):
        print("In iteration " + str(t))
        s1 = []
        s2 = []
        for row in matrix:
            for pixel in row:
                if pixel < t:
                    s1.append(pixel)
                else:
                    s2.append(pixel)
        var1 = np.nanvar(s1)
        var2 = np.nanvar(s2)
        results.append((var1 + var2) / 2)
    results = np.array(results)
    print("Variance array : " + str(results))
    min_var = sys.maxsize
    t = -1
    for index in range(len(results)):
        if not(math.isnan(results[index])) and min_var > results[index]:
            min_var = results[index]
            t = index
    # min_var = np.amin(results)
    print("Minimum variance: " + str(min_var))
    if len(np.where(results == t)) > 1:
        print("Warning: multiple t values found!")
    print("t: " + str(t))
    print("Partition starts...")
    s1 = np.array(matrix)
    s2 = np.array(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < t:
                s2[i][j] = 0
            else:
                s1[i][j] = 0
    s1 = np.array(s1)
    s2 = np.array(s2)
    print("Plotting now...")
    plt.imshow(s1)
    plt.show()
    plt.imshow(s2)
    plt.show()


def main():
    # convert the png into python matrix
    image1 = Image.open("img/otsu_1.jpg")
    image2 = Image.open("img/otsu_2.png")
    plt.style.use('grayscale')
    # t = 193
    matrix1 = np.array(image1)
    # t = 82
    matrix2 = np.array(image2)
    otsu_threshold(matrix1)
    otsu_threshold(matrix2)


if __name__ == "__main__":
    main()
