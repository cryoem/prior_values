import sys
sys.path.append('modules')
import numpy as np
import os as os
import calculations
import read_sphire
import read_star
import write_star


def combine_arrays(array_one, array_two):
    """Add column to input array"""

    assert(len(array_one) == len(array_two))
    dtype_one = array_one.dtype.descr
    dtype_two = array_two.dtype.descr
    dtype_new = dtype_one + dtype_two
    array_combined = np.empty(len(array_one), dtype=dtype_new)

    for name in array_one.dtype.names:
        array_combined[name] = array_one[name]
    for name in array_two.dtype.names:
        array_combined[name] = array_two[name]
    return array_combined


def add_column(array_ori, array_new, new_name):
    """Add column to input array"""

    dtype_new = array_ori.dtype.descr
    dtype_new.append((new_name, '<f8'))
    array_combined = np.empty(len(array_ori), dtype=dtype_new)

    for name in array_ori.dtype.names:
        array_combined[name] = array_ori[name]
    array_combined[new_name] = array_new
    return array_combined


def swap_columns(array, name_one, name_two):
    """Swap two columns of the array"""
    array = np.copy(array)
    array_temp = np.copy(array[name_one])
    array[name_one] = np.copy(array[name_two])
    array[name_two] = array_temp
    return array


def create_substack(array, indices):
    """Create a substack of an array"""

    new_array = np.empty(len(indices), dtype=array.dtype.descr)
    for idx, entry in enumerate(indices):
        for name in array.dtype.names:
            new_array[idx][name] = array[entry][name]

    return new_array

def main(file_name, tolerance, tolerance_filament, window_size, plot=False, typ='sphire', params=None):
    """Start calculation"""

    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0
        original_stack = read_sphire.get_sphire_stack(file_name)
        parameter = read_sphire.get_sphire_file('params', 'params.txt')
        indices = read_sphire.get_sphire_file('index', 'index.txt')
        substack = create_substack(original_stack, indices)
        array = combine_arrays(substack, parameter)
        id_name = 'filament'
        micrograph_name = 'ptcl_source_image'
        angle_name = 'phi'
        angle_name_new = 'phi_prior'
    elif typ == 'relion':
        angle_max = 180
        angle_min = -180
        array, header, path = read_star.import_star_file(file_name)
        id_name = '_rlnHelicalTubeID'
        micrograph_name = '_rlnMicrographName'
        angle_name = '_rlnAnglePsi'
        angle_name_new = '_rlnAnglePsiPrior'
    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    # Add the particle number to the array
    array_order = 'particle_order'
    order_numbers = np.arange(len(array))
    array = add_column(array, order_numbers, array_order)
    # Add rotated data column to the array
    data_rotated_name = 'data_rotated'
    array = add_column(array, array[angle_name], data_rotated_name)

    # Sort the array
    array = np.sort(array, order=[micrograph_name, id_name])

    filament_array = calculations.get_filaments(array, id_name)
    array_modified = None
    if plot:
        do_plot = True
    else:
        do_plot = False

    for idx, filament in enumerate(filament_array):
        if do_plot:
            if idx % 10000 == 0:
                plot = True
            else:
                plot = False
        if plot:
            calculations.plot_polar('raw_data', filament[data_rotated_name], 0, angle_max, 0)

        filament[data_rotated_name] = calculations.subtract_and_adjust_angles(filament[data_rotated_name], 0, 180, -180)
        filament[data_rotated_name], rotate_angle = calculations.rotate_angles(filament[data_rotated_name], plot)

        is_outlier, filament[data_rotated_name], rotate_angle, inside_tol_idx, outside_tol_idx = calculations.get_filament_outliers(
            data_rotated=filament[data_rotated_name],
            rotate_angle=rotate_angle,
            tolerance=tolerance,
            tolerance_filament=tolerance_filament,
            plot=plot
            )

        mean_array = calculations.calculate_mean_prior(
            input_array=filament[data_rotated_name],
            window_size=window_size,
            inside_tolerance_idx=inside_tol_idx,
            outside_tolerance_idx=outside_tol_idx,
            plot=plot
            )

        if plot:
            calculations.plot_polar('mean_array', mean_array, rotate_angle, 180, -180)

        mean_array = calculations.subtract_and_adjust_angles(
            mean_array, -rotate_angle, angle_max, angle_min
            )

        if plot:
            calculations.plot_polar('mean_array', mean_array, 0, angle_max, angle_min)

        filament = add_column(filament, mean_array, angle_name_new)

        if idx == 0:
            new_array = filament
        else:
            new_array = np.append(new_array, filament)

    # Sort the array back to the original order
    new_array = np.sort(array, order=array_order)



if __name__ == '__main__':
    plot = False
    if sys.argv[1] == 'relion':
        name = 'data_test.star'
        typ = 'relion'
        plot = True
    else:
        name = 'bdb:stack_small'
        typ = 'sphire'

    tolerance = 30
    tolerance_filament = 0.2
    window_size = 4

    main(
        file_name=name,
        tolerance=tolerance,
        tolerance_filament=tolerance_filament,
        window_size=window_size,
        typ=typ,
        plot=plot
        )
