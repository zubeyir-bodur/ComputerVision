import cv2 as cv
import os
import numpy as np
import copy
from scipy.spatial import distance
from PIL import Image
import matplotlib.pyplot as plt


def main(path_name, descriptor_choice):
    """
    Main entry point for the program. Warning, the program assumes image stitching in grayscale 2D images!
    :param path_name: Path to a text file that lists paths for the images to be stitched together
    :param descriptor_choice: One of two options, either SIFT or RPBD (Random pixel based descriptor)
    :return: None. But it will output the images stitched together in matplotlib
    """
    # 0. Input validation
    has_param_err = False
    if descriptor_choice != "gradient" and descriptor_choice != "raw":
        print("Wrong descriptor parameter.")
        has_param_err = True

    if not os.path.exists(path_name):
        print("The path " + path_name + " or " +
              os.path.dirname(os.path.abspath(__file__)) + "\\" + path_name + " does not exist.")
        has_param_err = True

    if not os.path.isfile(path_name):
        print("The path " + path_name + " or " +
              os.path.dirname(os.path.abspath(__file__)) + "\\" + path_name + " is not a file.")
        has_param_err = True

    if has_param_err:
        return

    image_paths = []
    with open(path_name) as f:
        image_paths = f.readlines()

    for i in range(len(image_paths)):
        if image_paths[i][len(image_paths[i])-1] == '\n':
            image_paths[i] = image_paths[i][:len(image_paths[i])-1]
        if (not os.path.isfile(image_paths[i])) and image_paths[i] != "":
            print("A given image path in the text file is not a file: " + image_paths[i])
            has_param_err = True

    if has_param_err:
        return

    # 1. Input validation ends, obtain a set of interest points using SIFT
    sift = cv.SIFT_create()
    key_points = []
    descriptors = []
    images = []
    for i in range(len(image_paths)):
        img = Image.open(image_paths[i])
        images.append(np.array(img))
        kp_cur = sift.detect(images[i])
        key_points.append([])
        # Check each feature, eliminate those whose diameter are very small
        for j in range(len(kp_cur)):
            feature = kp_cur[j]
            # Run feature selection at start
            # Let the threshold be 4.5 for the feature
            # size due to computation limits
            if feature.size >= 4.5:
                key_points[i].append(feature)
        # Show a key_pointed image
        temp_img = copy.deepcopy(images[0])
        temp_img = cv.drawKeypoints(image=images[i], keypoints=key_points[i], outImage=0,
                                    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        temp_img_pil = Image.fromarray(temp_img, mode='RGB')
        temp_img_pil.show()

    # 2. Use a descriptor for each feature.

    # 2.1. Use gradient based descriptor on the interest points gathered from step 1
    if descriptor_choice == "gradient":
        for i in range(len(image_paths)):
            des_cur = sift.compute(images[i], key_points[i])
            # des_cur is a 2-tuple, (key_points, descriptor)
            # we need the descriptor only,
            # as we already have the key_points

            # descriptors[i] := des_cur[1] -- of shape len(key_points[i]) X 128 --
            # descriptors[i] is the ith set of vectors for image[i]
            # where each of those vectors are of size 128
            descriptors.append(des_cur[1])
    # elif descriptor_choice == "raw":
    #    for i in range(len(image_paths)):
    #        for j in range(len(key_points)):
    # TODO
    #   2.2 Use raw pixel based descriptor on points gathered from step 1
    #       2.2.1 form a square around the pixel using the features gathered in 1
    #       2.2.2 form a 256 bin histogram to describe each point in this image

    # 3. Feature matching step
    #   3.1 Consider the euclidean distance between feature vectors
    for i in range(len(images) - 1):
        # check the pair images[i], images[i+1] for faster computations,
        # where i is ranging from 0 to n-1
        matches = []
        # distances = []
        T = 150.0
        M = 0
        for j in range(len(key_points[i])):
            for k in range(len(key_points[i+1])):
                dist = distance.euclidean(descriptors[i][j], descriptors[i+1][k])
                # distances.append(dist)
                #   3.2 If the distance is above a threshold T, those features match. Mark them as matching features
                #   for these pairs.
                #       3.2.1 Find a good T value, found using Otsu's thresholding idea.
                #               Use T = 120.0, reasons explained in the report
                if dist <= T:
                    #   3.3 Store the coordinates of pixels whose feature vectors in a pair of images match
                    matches.append((key_points[i][j].pt, key_points[i+1][k].pt))
            # 3.2.1 TODO Or for a given T, consider a minimum match count to decide if an image pair
            #           overlaps or not. If len(matches) < M, then stop computing this pair.
            #           And move on to the next one.

        """
        # define window size, output and axes
        fig, ax = plt.subplots(figsize=[8, 6])
        
        # set plot title
        ax.set_title("Histogram of Euclidean Distances Between Feature Vectors")

        # set x-axis name
        bins = 750
        ax.set_xlabel(f"Intervals, whose width is apx. {700/bins}")

        # set y-axis name
        ax.set_ylabel("Count")

        # create histogram within output
        N, bins, patches = ax.hist(distances, bins=bins, color="#777777")  # initial color of all bins

        # Iterate through all histogram elements
        # each element in this interation is one patch on the histogram, where:
        # - bin_size - number of records in current bin
        # - bin - value of current bin (x-axis)
        # - patch - a rectangle, object of class matplotlib.patches.Patch
        # more details on patch properties: [visit this link][1]
        for bin_size, bin, patch in zip(N, bins, patches):
            if bin <= T:
                patch.set_facecolor("#FF0000")
                patch.set_label("something")
        plt.show()
        """

    # 4. Image registration step, using RANSAC
    #   4.1 Parameter tuning in RANSAC

    # 5. Blending step.
    # 5.1 Examine 1: Averaging the pixel values in the overlapped regions from two or more images
    # 5.2 Examine 2: Weighted averaging of overlapping pixel values where the weights vary linearly
    #               according to the distance of a pixel in the overlapped region to the centre of
    #               either one of the images.

    # 6. Show the final image using PIL
    return


if __name__ == '__main__':
    print("Image stitching in Python." +
          "\nTo use it, enter two parameters, first one being the text file listing the image paths," +
          "\nthe second one is the option for descriptors in algorithm." +
          "\nType gradient (Gradient based descriptor) or raw (Random-pixel based descriptor).\n")
    path_name_main = input("Enter file name or full path: ")
    descriptor_choice_main = input("Descriptor choice, gradient or raw: ")
    main(path_name_main, descriptor_choice_main)
