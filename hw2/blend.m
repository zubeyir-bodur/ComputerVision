function dst_image = blend(panorama, overlapping_regions, code)
    % image_stitcher  Add two values together.
    %   dst_image = blend(path_name, overlapping_regions, "avg")
    %   blends the final output using simple averaging
    %
    %   dst_image = image_stitcher(path_name, overlapping_regions, "wavg")
    %   uses weighted averaging instead

    if (code == "avg")
        for k=1:size(overlapping_regions, 3)
            % Run M point averager on panorama w.r.t this overlapping region
            % Where M = 7
            M = 7;
            H = ones(7, 7, 'double') / M;

            % Find the limits of each overlapping region - TODO
            size_X_x = size(panorama, 2);
            size_X_y = size(panorama, 1);
            size_H_x = size(H, 2);
            size_H_y = size(H, 1);
            size_Y_x = size_X_x + size_H_x - 1;
            size_Y_y = size_X_y + size_H_y - 1;

            % Find the new indexes of the overlapping region
            dst_image = panorama(:, :);

            

            for j = 1:size_Y_y
                for i = 1:size_Y_x
                    for v = 1:size_H_y
                        for u = 1:size_H_x
                            % Average only if the regions overlap
                            if ( (j - v > 0) && (j - v <= size_X_y) && ...
                                    (i - u > 0) && (i - u <= size_X_x) ...
                                && overlapping_regions(j - v, i - u, k) )
                                dst_image(j, i) = dst_image(j, i) + H(v, u) * X(j - v, i - u);
                            end
                        end
                    end
                end
            end
        end
    elseif (code == "wavg")

    end
end