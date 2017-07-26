import sys
sys.path.append('/Users/stabrin/Desktop/prior_test/test_driven/modules')
import numpy as np
import scipy.stats as so
import os
from sparx import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_filaments(array, filament_name):
    """Calculate the size and members of each filament with numpy"""
    # Create a list of unique filament names with indices
    filament_names, inverse = np.unique(
        array[filament_name], return_inverse=True
        )
    # Loop through the indices and create subarrays
    filament_list = []
    for idx in range(len(filament_names)):
        indices_filament = np.where(inverse == idx)[0]
        filament_list.append(array[indices_filament])

    return np.array(filament_list)


def get_local_mean(input_array, rotate_angle, tolerance):
    """Calculate the local mean of the rotated array"""
    # Get the values of the outliers and non outliers
    inside_tolerance, outside_tolerance = get_tolerance_outliers(input_array, tolerance)

    # Calculate the local mean and rotate the coordinate system
    local_mean = np.mean(inside_tolerance)
    mean = subtract_and_adjust_angles(rotate_angle, -local_mean, 180, -180)
    subtract_and_adjust_angles(input_array, local_mean, 180, -180)

    return mean, len(outside_tolerance)


def rotate_angles(data_rotated, plot=False, output='.'):
    """Rotate angles to match 0 with the median"""
    if plot:
        plot_polar('raw_data', data_rotated, 0, 180, -180, output=output)

    # Calculate where the most angles are
    diff_from_zero = np.median(np.abs(data_rotated))
    nr_positive = len(data_rotated[data_rotated >= 0])
    nr_negative = len(data_rotated) - nr_positive
    if nr_negative > nr_positive:
        current_median = -diff_from_zero
    else:
        current_median = diff_from_zero

    if plot:
        plot_polar('absolut_values', np.abs(data_rotated), 0, 180, -180, output=output)
        plot_polar('absolut_values_diff_from_zero', np.abs(data_rotated), 0, 180, -180, mean=diff_from_zero, output=output)
        plot_polar('absolut_values_diff_from_zero', data_rotated, 0, 180, -180, mean=diff_from_zero, output=output)

    iteration = 0
    rotate_angle = current_median
    current_median_old = current_median
    if plot:
        plot_polar('current_median', data_rotated, 0, 360, 0, mean=rotate_angle, output=output)

    while iteration < 100:
        # In place subtraction
        subtract_and_adjust_angles(data_rotated, current_median, 180, -180)
        # Use the median for uneven numbers and the left median for even
        if len(data_rotated) % 2 == 0:
            median = np.sort(data_rotated)[len(data_rotated)//2]
        else:
            median = np.median(data_rotated)
        # Caluclate the new rotation angle
        rotate_angle = subtract_and_adjust_angles(rotate_angle, -median, 180, -180)
        if iteration == 0 and plot:
            plot_polar('current_median_{0}'.format(iteration), data_rotated, current_median, 180, -180, mean=median, old_mean=0, output=output)

        # Check abort criteria
        if median == 0:
            break
        elif median == current_median_old:
            break
        else:
            current_median_old = current_median
            current_median = median
        iteration += 1

    if plot:
        plot_polar('rotated_data_median', data_rotated, rotate_angle, 180, -180, old_mean=0, output=output)

    return rotate_angle


def subtract_and_adjust_angles(data_subtracted, value, angle_max, angle_min):
    """Subtract a value from an angle and adjust the angle range"""
    if isinstance(data_subtracted, np.int64) or \
            isinstance(data_subtracted, np.float64):
        data_subtracted = np.subtract(data_subtracted, value)
        if data_subtracted > angle_max:
            data_subtracted -= 360
        elif data_subtracted <= angle_min:
            data_subtracted += 360
        else:
            pass
        return data_subtracted

    elif isinstance(data_subtracted, np.ndarray):
        np.subtract(data_subtracted, value, out=data_subtracted)
        np.subtract(data_subtracted, 360, out=data_subtracted, where=data_subtracted>angle_max)
        np.add(data_subtracted, 360, out=data_subtracted, where=data_subtracted<angle_min)
        return None

    else:
        assert(False)


def get_filament_outliers(data_rotated, rotate_angle, tolerance, tolerance_filament, plot=False, output='.'):
    """Get filament outliers based on tolerance"""

    if plot:
        plot_polar('rotated_data_for_mean', data_rotated, rotate_angle, 180, -180, old_mean=0, tol=tolerance, mean=0, output=output)
        plot_rotate_angle = rotate_angle

    # Calculate the local mean
    rotate_angle, nr_outliers = get_local_mean(
        data_rotated,
        rotate_angle,
        tolerance
        )
    rotate_angle_old = rotate_angle
    iteration = 0
    while iteration < 100:
        # Calculate the local mean
        rotate_angle, nr_outliers = get_local_mean(
            data_rotated,
            rotate_angle,
            tolerance
            )

        # Abort criteria
        if rotate_angle == rotate_angle_old:
            break
        else:
            rotate_angle_old = rotate_angle
        iteration += 1

    if plot:
        plot_polar('rotated_data_mean', data_rotated, rotate_angle, 180, -180, mean=0, tol=tolerance, old_mean=plot_rotate_angle-rotate_angle_old, output=output)
    inside_tolerance_idx, outside_tolerance_idx = find_tolerance_outliers(
        data_rotated, tolerance, nr_outliers
        )

    if nr_outliers / float(len(data_rotated)) >= tolerance_filament:
        outlier = True
    else:
        outlier = False

    return outlier, rotate_angle, inside_tolerance_idx, outside_tolerance_idx


def get_tolerance_outliers(input_array, tolerance):
    """Calculate the outliers"""
    inside_tolerance = input_array[np.logical_and(
        input_array >= -tolerance,
        input_array <= tolerance
        )]
    outside_tolerance = input_array[np.logical_or(
        input_array <= -tolerance,
        input_array >= tolerance
        )]

    return inside_tolerance, outside_tolerance


def find_tolerance_outliers(input_array, tolerance, nr_outliers):
    """Calculate the outliers"""
    if nr_outliers < len(input_array)/float(2):
        outside_tolerance = np.where(np.logical_or(
            input_array < -tolerance,
            input_array > tolerance
            ))[0]
        inside_tolerance = np.array(
            [i for i in range(len(input_array)) if i not in outside_tolerance]
            )
    else:
        inside_tolerance = np.where(np.logical_and(
            input_array >= -tolerance,
            input_array <= tolerance
            ))[0]
        outside_tolerance = np.array(
            [i for i in range(len(input_array)) if i not in inside_tolerance]
            )

    return inside_tolerance, outside_tolerance


index_fit = 0
def calculate_mean_prior(input_array, mean_array, window_size, inside_tolerance_idx, outside_tolerance_idx, plot=False, output='.'):
    """Calculate running mean of the filament array"""

    if window_size < 3:
        print("Window size needs to be at least 3: Changed window size to 3 and continue")
        window_size = 3

    if len(inside_tolerance_idx) <= window_size * 1.5:
        mean_array.fill(0)
    else:
        mean_list = []
        mean_x_list = []
        number_of_means = len(input_array) - window_size + 1
        if window_size / float(2) % 2 == 0:
            min_x_mean = window_size / float(2) - 0.5
        else:
            min_x_mean = window_size // float(2)

        inside_tolerance_idx = set(inside_tolerance_idx)
        for mean_idx in range(number_of_means):
            summation = 0
            skip = 0
            for number_idx in range(mean_idx, mean_idx + window_size):
                if number_idx in inside_tolerance_idx:
                    summation += input_array[number_idx]
                else:
                    assert(number_idx in outside_tolerance_idx)
                    skip += 1
            if skip == window_size:
                continue
            else:
                mean_value = summation / float(window_size - skip)
                mean_list.append(mean_value)
                mean_x_list.append(min_x_mean + mean_idx)

        mean_for_fit = np.array(mean_list)
        x_values_fit = np.array(mean_x_list)
        slope, intercept, rvalue, pvalue, stderr = so.linregress(x_values_fit, mean_for_fit)

        x_values_fit_mean = np.mean(x_values_fit)
        x_values_fit_variance = np.sum((x_values_fit - x_values_fit_mean)**2)
        slope_sd = stderr * np.sqrt(1/float(len(x_values_fit)) + x_values_fit_mean**2/x_values_fit_variance)
        intercept_sd = stderr * np.sqrt(1/x_values_fit_variance)

        for idx in range(len(input_array)):
            mean_array[idx] = slope * idx + intercept

        if plot:
            global index_fit
            plt.plot(x_values_fit, mean_for_fit, 'x', label='running averages')
            plt.plot(range(len(input_array)), input_array, 'o', label='data')
            x = np.linspace(0, len(input_array)-1, 10000)
            plt.plot(x, slope * x + intercept, label='linear regression')
            plt.ylim([-30, 30])
            plt.legend(loc='best')
            plt.xlabel('Particle helix id')
            plt.ylabel('Relative angle / degree')
            plt.grid()
            plt.savefig('{0}/pics/fit_{1}.png'.format(output, index_fit))
            plt.clf()
            index_fit += 1

    return mean_array

index_plot = 0
def plot_polar(name, array, angle_rotation, angle_max, angle_min, mean=None, tol=None, label=None, old_mean=None, output='.'):
    """Do a polar plot"""
    global index_plot
    # radar green, solid grid lines
    plt.rc('grid', color='#316931', linewidth=1, linestyle='-')
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)

    # force square figure and square axes looks better for polar, IMO
    width, height = matplotlib.rcParams['figure.figsize']
    size = min(width, height)

    # make a square figure
    fig = plt.figure(figsize=(size, size))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, axisbg='#d5de9c')

    # Change the labels
    ax.set_yticklabels([])
    ax.set_theta_direction(-1)
    offset = -np.radians(angle_rotation) + np.pi/2
    ax.set_theta_offset(offset)
    if angle_max == 360:
        labels = [str(item) if item != 360 else str(0) for item in np.linspace(0, 360, 9) if item >= angle_min]
    elif angle_max == 180:
        labels = [str(item-360) if item > 180 else str(item) for item in np.linspace(0, 360, 9) if item >= angle_min]
    else:
        labels = [str(item) if item != 360 else str(0) for item in np.linspace(angle_min, angle_max, 9) if item >= angle_min]
    ax.set_xticklabels(labels)

    # Plot the data
    color = plt.cm.Dark2(np.linspace(0, 1, len(array)))
    for idx in range(len(array)):
        plt.arrow(np.radians(array[idx]), 0.01, 0, 0.9, alpha=1, width=0.005, edgecolor=color[idx], facecolor=color[idx], lw=2, zorder=5)

    if mean is not None:
        plt.arrow(np.radians(mean), 0.01, 0, 0.9, alpha=1, width=0.005, edgecolor='black', facecolor='black', lw=4, zorder=5)

    if old_mean is not None:
        plt.arrow(np.radians(old_mean), 0.01, 0, 0.7, alpha=1, width=0.005, edgecolor='blue', facecolor='blue', lw=4, zorder=5)

    if tol is not None:
        plt.arrow(np.radians(mean+tol), 0.01, 0, 0.5, alpha=0.5, width=0.005, edgecolor='black', facecolor='black', lw=2, zorder=5)
        plt.arrow(np.radians(mean-tol), 0.01, 0, 0.5, alpha=0.5, width=0.005, edgecolor='black', facecolor='black', lw=2, zorder=5)

    # Beautify
    #plt.title('{0} {1}'.format(np.max(array), np.min(array)))
    if not os.path.exists(output):
        os.mkdir(output)
    out_dir = '{0}/pics'.format(output)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    plt.savefig('{0}/{1:02d}_{2}.png'.format(out_dir, index_plot, name))
    index_plot += 1
    plt.close(fig)
