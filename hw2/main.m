disp("IMPORTANT NOTE: PLEASE ENTER QUOTES WHILE ENTERING INPUT!");
disp("E.G.: USE " + '"' + "test1.txt" + '"' + " INSTEAD OF test1.txt");
disp(newline + "IN ADDITION, IN EACH RUN, IT IS IMPORTANT TO CLEAR THE WORKSPACE AS WELL" + newline);
disp(newline + "Image stitching in MATLAB." + newline);
disp("To use it, enter two parameters," + newline ...
    + "first one being the text file listing the image paths,");
disp("the second one is the option for descriptors in algorithm.");
disp("Type " + '"' + "gra" + '"' ...
    + "(Gradient based descriptor) or " ...
    + '"' + "raw" + '"' ...
    + " (Raw-pixel based descriptor)." + newline);
path_name_main = input("Enter file name or full path: ");
descriptor_choice_main = input("Descriptor choice, gradient or raw: ");
[panorama, overlapping_regions] = image_stitcher(path_name_main, descriptor_choice_main);
imshow(panorama, []);
% panorama_prime = blend(panorama, overlapping_regions, "avg");
% panorama_w_prime = blend(panorama, overlapping_regions, "wavg");