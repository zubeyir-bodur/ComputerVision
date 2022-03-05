"""
  Computer Vision HW 1 - Question 3
"""
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def otsu_threshold():
    """
    Otsu Threshold from scratch:
    Separates background & foreground from an image

    Will use GUROBI to find the threshold t, that solves
    the linear minimization problem:
        Minimize var1 + var2 s.t.
            t is within [0, 255] range, and separates group1 & 2.
            where var1 is computed from the image matrix w/ numpy.var

    Then will separate two groups into two images:
        e.g. from group 1, remove all pixels that do not
        belong to group 1. same for group 2

    Then, will display those image matrices in matplotlib
    :return
    """
    return


def main():
    return


if __name__ == "__main__":
    main()
