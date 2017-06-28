import sys
sys.path.append('/Users/stabrin/Desktop/prior_test/test_driven/modules')
import numpy as np
import scipy.stats as so
import os
#import matplotlib.pylab as plt


def get_filaments(array, id_name):
    """Calculate the size and members of each filament"""
    filaments = []
    current_id = array[id_name][0]
    current_filament = []

    for entry in array:
        if entry[id_name] != current_id:
            current_id = entry[id_name]
            filaments.append(np.array(current_filament))
            current_filament = []
            current_filament.append(entry)
        else:
            current_filament.append(entry)

    filaments.append(np.array(current_filament))

    return np.array(filaments)


def get_local_mean(input_array, rotate_angle, tolerance, angle_max, angle_min):
    """Calculate the local mean"""
    inside_tolerance, outside_tolerance = get_tolerance_outliers(input_array, tolerance)

    local_mean = np.mean(inside_tolerance)

    mean = subtract_and_adjust_angles(rotate_angle, local_mean, angle_max, angle_min)
    data_rotated = subtract_and_adjust_angles(input_array, local_mean, angle_max, angle_min)
    assert(angle_min <= mean <= angle_max, input_array, rotate_angle)

    return data_rotated, mean, len(outside_tolerance)


def rotate_angles(array, angle_max, angle_min):
    """Rotate angles to match the median"""

    diff_from_zero = np.mean(np.abs(array))
    nr_positive = len(array[array >= 0])
    nr_negative = len(array) - nr_positive
    data_rotated = np.copy(array)

    if diff_from_zero > 90:
        for idx in range(len(data_rotated)):
            if data_rotated[idx] < 0:
                data_rotated[idx] = data_rotated[idx] + 360
            else:
                pass
    else:
        pass

    if nr_negative > nr_positive:
        current_median = -diff_from_zero
    else:
        current_median = diff_from_zero

    iteration = 0
    rotate_angle = current_median
    current_median_old = current_median

    while iteration < 100:
        data_rotated = subtract_and_adjust_angles(data_rotated, current_median, angle_max, angle_min)
        median = np.median(data_rotated)
        rotate_angle += median

        if median == 0:
            break
        elif median == current_median_old:
            break
        else:
            current_median_old = current_median
            current_median = median

        iteration += 1

    rotate_angle = subtract_and_adjust_angles(rotate_angle, 0, angle_max, angle_min)

    return data_rotated, rotate_angle


def subtract_and_adjust_angles(input_data, value, angle_max, angle_min):
    """Subtract a value from an angle"""
    data_subtracted = np.subtract(input_data, value)
    if isinstance(data_subtracted, np.int64) or \
            isinstance(data_subtracted, np.float64):
        if data_subtracted > angle_max:
            data_subtracted -= 360
        elif data_subtracted <= angle_min:
            data_subtracted += 360
        else:
            pass
    elif isinstance(data_subtracted, np.ndarray):
        for idx in range(len(data_subtracted)):
            if data_subtracted[idx] >= angle_max:
                data_subtracted[idx] = data_subtracted[idx] - 360
            elif data_subtracted[idx] < angle_min:
                data_subtracted[idx] = data_subtracted[idx] + 360
            else:
                pass
    else:
        assert(False, 'Unreachable code')

    return data_subtracted


def get_filament_outliers(data_rotated, rotate_angle, tolerance, tolerance_filament, angle_max, angle_min):
    """Get filament outliers based on tolerance"""

    data_rotated, rotate_angle, nr_outliers = get_local_mean(
        data_rotated,
        rotate_angle,
        tolerance,
        angle_max,
        angle_min
        )
    rotate_angle_old = rotate_angle
    iterations = 0
    while iterations < 100:
        data_rotated, rotate_angle, nr_outliers = get_local_mean(
            data_rotated,
            rotate_angle,
            tolerance,
            angle_max,
            angle_min
            )

        if rotate_angle == rotate_angle_old:
            break
        else:
            rotate_angle_old = rotate_angle

        iterations += 1

    inside_tolerance_idx, outside_tolerance_idx = find_tolerance_outliers(
        data_rotated, tolerance
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


def find_tolerance_outliers(input_array, tolerance):
    """Calculate the outliers"""
    inside_tolerance = np.where(np.logical_and(
        input_array >= -tolerance,
        input_array <= tolerance
        ))
    outside_tolerance = np.where(np.logical_or(
        input_array <= -tolerance,
        input_array >= tolerance
        ))

    return inside_tolerance[0], outside_tolerance[0]


def calculate_mean_prior(input_array, window_size, inside_tolerance_idx, outside_tolerance_idx, rotate_angle, angle_max, angle_min):
    """Calculate running mean of the filament array"""

    mean_array = np.empty(len(input_array))
    if window_size < 3:
        print("Window size needs to be at least 3: Changed window size to 3 and continue")
        window_size = 3

    if len(inside_tolerance_idx) <= window_size * 1.5:
        for idx in range(len(input_array)):
            mean_array[idx] = 0
    else:
        mean_list = []
        mean_x_list = []
        number_of_means = len(input_array) - window_size + 1
        min_x_mean = window_size // 2

        for mean_idx in range(number_of_means):
            summation = 0
            skip = 0
            for number_idx in range(mean_idx, mean_idx + window_size):
                if number_idx in inside_tolerance_idx:
                    print(number_idx)
                    summation += input_array[number_idx]
                else:
                    assert(number_idx in outside_tolerance_idx)
                    skip += 1
            if skip == window_size:
                continue
            else:
                mean_value = summation / float(window_size)
                mean_list.append(mean_value)
                mean_x_list.append(min_x_mean + mean_idx)

        mean_for_fit = np.array(mean_list)
        x_values_fit = np.array(mean_x_list)
        slope, intercept, rvalue, pvalue, stderr = so.linregress(x_values_fit, mean_for_fit)

        for idx in range(len(input_array)):
            mean_array[idx] = slope * idx + intercept

        #plt.plot(x_values_fit, mean_for_fit, 'x')
        #plt.plot(range(len(input_array)), input_array, 'o')
        #x = np.linspace(0, len(input_array)-1, 10000)
        #plt.plot(x, slope * x + intercept)
        #plt.ylim([-30, 30])
        #plt.title(rotate_angle)
        #plt.show()

    mean_array = subtract_and_adjust_angles(mean_array, -rotate_angle, angle_max, angle_min)

    return mean_array


def main():
    """Start calculation"""
    pass


if __name__ == '__main__':
    main()
