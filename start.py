import sys
sys.path.append('modules')
import numpy as np
import os as os
import calculations
import read_sphire
import read_star
import write_star


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


def main(file_name, tolerance, tolerance_filament, window_size, typ='sphire'):
    """Start calculation"""

    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0
        original_stack = read_sphire.get_sphire_stack(file_name)
        array = original_stack
        id_name = 'filament'
        angle_name = 'source_n'
        angle_name_new = 'source_n_pre_prior'
    elif typ == 'relion':
        angle_max = 180
        angle_min = -180
        array, header, path = read_star.import_star_file(file_name)
        id_name = '_rlnHelicalTubeID'
        angle_name = '_rlnAnglePsi'
        angle_name_new = '_rlnAnglePsiPrior'
    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    filament_array = calculations.get_filaments(array, id_name)
    array_modified = None

    for idx, filament in enumerate(filament_array):
        data_rotated, rotate_angle = calculations.rotate_angles(filament[angle_name], angle_max, angle_min)

        is_outlier, data_rotated, rotate_angle, inside_tol_idx, outside_tol_idx = calculations.get_filament_outliers(
            data_rotated=data_rotated,
            rotate_angle=rotate_angle,
            tolerance=tolerance,
            tolerance_filament=tolerance_filament
            )

        mean_array = calculations.calculate_mean_prior(
            input_array=data_rotated,
            window_size=window_size,
            inside_tolerance_idx=inside_tol_idx,
            outside_tolerance_idx=outside_tol_idx,
            rotate_angle=rotate_angle,
            angle_max=angle_max,
            angle_min=angle_min
            )

        filament = add_column(filament, mean_array, angle_name_new)
        if typ == 'sphire':
            filament = swap_columns(filament, angle_name, angle_name_new)
        else:
            pass

        if idx == 0:
            new_array = filament
        else:
            new_array = np.append(new_array, filament)


if __name__ == '__main__':
    name = 'bdb:stack_small'
    tolerance = 30
    tolerance_filament = 0.25
    window_size = 4
    typ = 'sphire'
    start.main(
        file_name=name,
        tolerance=tolerance,
        tolerance_filament=tolerance_filament,
        window_size=window_size,
        typ=typ
        )
