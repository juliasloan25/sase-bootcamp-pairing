from PIL import Image
import numpy as np
import sys

def main():
    # taking command line args
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    ink_limit = int(sys.argv[3])

    # TODO check arguments

    img = Image.open(input_path, 'r')
    arr = np.asarray(img)

    # Apply ink limiting function to all points in image
    output_arr = limit_image(arr.copy(), ink_limit)

    # Create output image in .tiff format
    output_img = Image.fromarray(output_arr, mode='CMYK')
    output_img.save(output_path, compression='tiff_deflate')


# Apply ink limiting function to all points in image
def limit_image(img_arr, ink_limit):
    # TODO vectorize limit_point function instead of for loops
    for i in range(len(img_arr)):
        for j in range(len(img_arr[0])):
            img_arr[i, j] = limit_point(img_arr[i, j], ink_limit)

    return img_arr


# Limit ink for an individual point
def limit_point(point, ink_limit):
    cmy_range = range(3)
    percent_point = map(convert_to_percent, point)

    # If ink limit is not exceeded, just return
    if sum(percent_point) <= ink_limit:
        return point

    # First combine CMY values into black
    min_cmy = min(percent_point[cmy_range])

    for i in cmy_range:
        percent_point[i] -= min_cmy
    percent_point[3] += min_cmy

    # If ink limit is not exceeded, return modified point
    if sum(percent_point) <= ink_limit:
        return convert_from_percent(percent_point)

    # TODO finish limiting


# Convert number in range [0, 255] to [0, 100]
def convert_to_percent(integer):
    return 100*integer/255

# Convert number in range [0, 100] to [0, 255]
def convert_from_percent(percent):
    return int(255*percent/100)

if __name__ == "__main__":
    main()