import numpy as np
import cv2
import matplotlib.pyplot as plt  # Only used for debug imaging
import os
import time
from multiprocessing.pool import ThreadPool
import errno

DEBUG = False
RUN_TIMING = False


# Take data, plot it, and return a numpy array of the plotted graph image
def data2np(graph_data, line_format='-'):
    # Generate a figure with matplotlib
    fig = plt.figure()
    plot = fig.add_subplot(111)

    # Resize
    fig.set_size_inches(7, 5)

    # Plot the data and draw the canvas
    plot.plot(graph_data, line_format)
    fig.tight_layout(pad=0)  # Reduce the white border
    fig.canvas.draw()  # It must be drawn before we can extract it

    # Now we can save it to a numpy array.
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # Cleanup
    plt.clf()
    plt.close(fig)

    return data


def build_filters(orientations=16, ksize=31):
    """
    Builds the filters using the values for ksize and # of orientations

    :param orientations:    The number of directional vectors to generate kernals for
    :param ksize:           The size of the Region to use for generating the vectors
    :return:                Gabor filters to use on the ROI
    """
    filters = []
    for theta in np.arange(0, np.pi, np.pi / orientations):
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        kern /= 1.5*kern.sum()
        filters.append(kern)
    return filters


def process_threaded(img, filters):
    """
    Run the Gabor kernal filters on the ROI (which is the img), to generate the output pixel directions for each kernal

    :param img:         ROI - Region Of Interest to run the filters on.
    :param filters:     The filters that were generated by the build_filters method
    :return:            combined image max for each filter, and the individual results for each kernal orientation
    """
    kernal_results = np.empty((len(filters), img.shape[0], img.shape[1]), dtype=np.uint8)

    combined = np.zeros_like(img)
    kern_index = 0
    def f(kern):
        return cv2.filter2D(img, cv2.CV_8UC3, kern)

    pool = ThreadPool(processes=4)
    for fimg in pool.map(f, filters):
        kernal_results[kern_index, :, :] = fimg  # Put the image into an array we can use it outside
        kern_index += 1
        np.maximum(combined, fimg, combined)
    pool.close()
    pool.join()

    return combined, kernal_results


def run_gabor(color_image, filters, image_filename, orientations=16, mode='training'):
    """
    Takes a source input image, runs the gabor filters on it, associates the location with a banded mask region,
        and saves it

    :param color_image:     The image to extract features from
    :param filters:         The return results from build_filters
    :param image_filename:  Name of the color_image file
    :param orientations:    Number of directions/orientations to split 360 into
    :param mode:            training/validation:
                                training = generate and save ROI Gabor extracted histograms
                                validation = Get Gabor histograms and return them for later use by an ANN to validate
    :return:                Complete set of all Histograms for the input color_image
    """
    directory, filename = os.path.split(image_filename)
    filename_minus_ext, ext = os.path.splitext(filename)

    # Convert to grayscale so we don't get multiple "votes" per pixel per kernal/orientation
    img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # run each of the N Gabor kernals (directions) once across the entire image producing N images (one for each direction/kernal)
    combined_image, kernal_results = process_threaded(img, filters)

    # From those, at each pixel position, take the maximum response at that position indicating the "direction" of that pixel. 0, 1, 2, .... , N
    # produce an array with these direction values for each pixel
    pixel_directions = np.argmax(kernal_results, axis=0)
    pixel_directions = pixel_directions.astype(np.uint8)

    all_gabors = []

    # grab ROI from the produced array (say 45x45, or whatever)
    roi_size_y = color_image.shape[0]
    roi_size_x = color_image.shape[1]
    roi_size = (roi_size_y, roi_size_x)
    for y in range(0, pixel_directions.shape[0], roi_size[0]):
        for x in range(0, pixel_directions.shape[1], roi_size[1]):

            # calculate/Count up the total of each value in image as a histogram of directions in the image
            roi = pixel_directions[y:y + roi_size[0], x:x + roi_size[1]]
            unique, unique_counts = np.unique(roi, return_counts=True)

            # A region may not always have values for ALL bins, so create an array and place what we get in it
            bins = np.zeros((orientations,))
            bins[unique] = unique_counts

            # Generate color histogram
            all_gabors.append(bins)

    # run the data from the files through ANN
    return np.vstack(all_gabors)

def display_histogram(bins, color_image, combined_image, img, roi, roi_size, x, y):
    """
    This is used mainly for debugging and visualization of the Hisogram and Gabor information on a Region from an image.
    Displays an image in a plot on the screen

    :param bins:            # of bins or "orientations" used for the histogram
    :param color_image:     The image that the histogram is being run on
    :param combined_image:  The combined max value image of all activated gabor kernals
    :param img:             Greyscale image of the color_image
    :param roi:             Argmax pixel values Region from the N kernal activations (This is the bin each pixels direction is)
    :param roi_size:        size of the Region of Interest
    :param x:               Where in the image should we snag the starting ROI X
    :param y:               Where in the image should we snag the starting ROI Y
    """
    # Plot and draw the bins histogram, then convert to numpy array
    result = data2np(bins)

    # Get the ROI for the items we are going to show the user
    gray_roi = img[y:y + roi_size[0], x:x + roi_size[1]]  # Get the greyscale ROI
    max_roi = combined_image[y:y + roi_size[0], x:x + roi_size[1]]  # Get max value per pixel in region for all Kernals
    roi_color = color_image[y:y + roi_size[0], x:x + roi_size[1]]

    # Exaggerate the ROI orientation pixel direction values for viewing
    sample = (roi + 1) * 15

    # Combine the three single channel color images
    stacked = np.hstack((gray_roi, max_roi, sample))

    # Resize them so they are larger
    stacked = cv2.resize(stacked, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    roi_color = cv2.resize(roi_color, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Replace the pixel values in the upper right corner with the stacked image
    result[5:stacked.shape[0] + 5, -(5 + stacked.shape[1]):-5, 0] = stacked
    result[5:stacked.shape[0] + 5, -(5 + stacked.shape[1]):-5, 1] = stacked
    result[5:stacked.shape[0] + 5, -(5 + stacked.shape[1]):-5, 2] = stacked

    # Add the color image to the upper right
    result[5:stacked.shape[0] + 5, -(5 + stacked.shape[1] + roi_color.shape[1]):-(5 + stacked.shape[1])] = roi_color

    # Display it all
    cv2.imshow('chart', result)
    cv2.waitKey()
    cv2.destroyAllWindows()


def create_color_histogram(image, bins=8):
    """
    Calculates the Color histogram for an image and returns a 3 element Python array of arrays of size bins
    The size of each array element is [(blues),(greens),(reds)].  Where (color) length = bins count.

    :param image: any size image to perform the histogram on
    :param bins: (default: 8) - the number of separate slots/groups/bins.  8 means 0-7 is bin 1, 8-15 is bin 2, etc
    :return: A Python List of length 3, where each element contains an array of bin values for that color channel.
    """

    colors = []
    # Loop over the three colors (Blue, Green, Red) (OpenCV has this order)
    for i in range(0, 3):
        colors.append(cv2.calcHist([image], [i], None, [bins], [0, 256]))

    return colors


# Save the hog information for a single HOG/Region
# Along with the coordinates, and the band prediction.
def save_hogs(hog_info, region_coords, band, output_file, color_hist=None):
    """
    Saves the HOG generated from the single ROI to the file

    :param hog_info: the data from the HOG to be saved
    :param region_coords: The X,Y position of the upper left of the ROI
    :param band: This is the "Y" value or prediction/category/classification
    :param output_file: already opened file to save to
    :return: nothing
    """
    csv_hog_info = ','.join([('%f' % num).rstrip('0').rstrip('.') for num in hog_info])
    csv_region_coords = ','.join(['%d' % num for num in region_coords])

    output_file.write(str(band))
    output_file.write(',')
    output_file.write(str(csv_hog_info))
    output_file.write(',')

    if color_hist is not None:
        csv_color_hist = ','.join([('%f' % num).rstrip('0').rstrip('.') for num in color_hist])
        output_file.write(str(csv_color_hist))
        output_file.write(',')

    output_file.write(str(csv_region_coords))
    output_file.write('\n')


def load_hogs_csv(directory):
    """
    Retrieves the data from all files in a folder, and returns the data and filenames

    :param directory: A string that represents the path of the folder containing the hog files
    :return: An ndarray containing the all the instances of the hog data, the coordinates, bands
    """
    all_hogs = []

    # Load images from folders in loop
    for filename in os.listdir(directory):
        combined_filename = os.path.join(directory, filename)
        print("Loading:", filename)
        all_hogs.append(np.loadtxt(combined_filename, delimiter=','))

    all_hogs = np.vstack(all_hogs)

    return all_hogs


def resize_image_to_mask(image, mask):
    """
    If an image size does not match the mask, resize the image to match the mask.

    :param image:   Image to run through Gabor Filter activations
    :param mask:    The mask that is used to determine which bands each ROI belongs to
    :return:        The resized image
    """
    r = mask.shape[1] / image.shape[1]
    dim = (mask.shape[1], int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized


def run_gabor_on_directory(directory, mask):
    """
    Using an input directory, run the Gabor filter feature extraction on each image in that directory,
        saving the results to a csv file for later us in the neural network file.

    :param directory:   Location where images are that need to be used to TRAIN the ANN
    :param mask:        mask used to decide which part of an image belongs to what cateogry/band.
    """
    start_time = time.time()

    orientations = 16
    filters = build_filters(orientations)

    for filename in os.listdir(directory):
        print("Start: ", filename)
        combined_filename = os.path.join(directory, filename)
        image_color = cv2.imread(combined_filename)

        # Make sure the image was loaded, if not, probably an invalid file format (text file?)
        if image_color is None:
            print('Invalid file:', filename)
            continue

        # Generate and save ALL hogs for this image
        result = run_gabor(image_color, filters, combined_filename, orientations, mode='training')

    print("Total Runtime:", time.time() - start_time)


'''
if __name__ == '__main__':
    mask_filename = r"../mask_generator/gray-mask.png"

    # real mask
    mask = cv2.imread(mask_filename, cv2.IMREAD_GRAYSCALE)

    run_gabor_on_directory(r'../images/', mask)
'''

