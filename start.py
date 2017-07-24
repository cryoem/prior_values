import sys
sys.path.append('modules')
sys.path.append('/work1/home/stabrin/Jasp_cLys_ADP/prior_values/modules')
import numpy as np
import os as os
import time
#import calculations
import read_sphire
#import read_star
#import write_star
#import write_sphire


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


def create_substack(array, indices):
    """Create a substack of an array"""
    new_array = array[indices]
    return new_array


def main(file_name, tolerance_psi, tolerance_theta, tolerance_filament, window_size, plot=False, typ='sphire', params=None, index=None, output_dir=None):
    """Start calculation"""

    if output_dir is None:
        output_dir = '.'

    if plot:
        do_plot = True
    else:
        do_plot = False


    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0

        original_stack = read_sphire.get_sphire_stack(file_name)
        parameter = read_sphire.get_sphire_file('params', params)
        indices = read_sphire.get_sphire_file('index', index)

        substack = create_substack(original_stack, indices)
        array = combine_arrays(substack, parameter)

        stack_id, mic_name, filament_name, particle_id = \
            original_stack.dtype.names

        angle_name = [
            ['psi', 'psi_prior', 'psi_rot'],
            ['theta', 'theta_prior', 'theta_rot']
            ]

        output_names = list(parameter.dtype.names)

    elif typ == 'relion':
        angle_max = 180
        angle_min = -180

        array, header, path = read_star.import_star_file(file_name)

        filament_name = '_rlnHelicalTubeID'
        mic_name = '_rlnMicrographName'
        particle_id = '_rlnImageName'
        angle_name = [
            ['_rlnAnglePsi', '_rlnAnglePsiPrior', '_rlnAnglePsiRotated'],
            ['_rlnAngleTilt', '_rlnAngleTiltPrior', '_rlnAngleTiltRotated']
            ]

        output_names = list(array.dtype.names)

    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    # Add new angle names to the output dtype
    IDX_OLD = 0
    IDX_NEW = 1
    IDX_ROT = 2
    dtype_temp = array.dtype.descr
    for angle in angle_name:
        dtype_temp.append((angle[IDX_NEW], '<f8'))
        dtype_temp.append((angle[IDX_ROT], '<f8'))
        output_names.append(angle[IDX_NEW])

    # Create a new combined array
    array_temp = np.empty(len(array), dtype=dtype_temp)
    for angle in angle_name:
        array_temp[angle[IDX_ROT]] = np.copy(array[angle[IDX_OLD]])

    # Sort the array
    array = np.sort(array_temp, order=[mic_name, filament_name, particle_id])

    # Split the array into filaments
    filament_array = calculations.get_filaments(array[filament_name])

    idx_sub = 0
    idx_rotate = 1
    idx_outlier = 2
    idx_mean = 3
    idx_sub_2 = 4
    idx_add = 5
    idx_add_2 = 6
    for angle, tolerance in zip(angle_name, [tolerance_psi, tolerance_theta]):
        time_list = [[] for i in range(7)]
        for idx, filament in enumerate(filament_array):
            if do_plot:
                if idx % 10000 == 0:
                    plot = True
                else:
                    plot = False
            if idx % 10000 == 0:
                print('{0}%'.format(idx * 100/ len(filament_array)), len(filament_array))
                plot = True
            else:
                plot = False
            if plot:
                calculations.plot_polar('raw_data', filament[data_rotated_name], 0, angle_max, 0, output=output_dir)

            start = time.time()
            filament[data_rotated_name] = calculations.subtract_and_adjust_angles(filament[data_rotated_name], 0, 180, -180)
            time_list[idx_sub].append(time.time() - start)
            start = time.time()
            filament[data_rotated_name], rotate_angle = calculations.rotate_angles(filament[data_rotated_name], plot, output=output_dir)
            time_list[idx_rotate].append(time.time() - start)

            start = time.time()
            is_outlier, filament[data_rotated_name], rotate_angle, inside_tol_idx, outside_tol_idx = calculations.get_filament_outliers(
                data_rotated=filament[data_rotated_name],
                rotate_angle=rotate_angle,
                tolerance=tolerance,
                tolerance_filament=tolerance_filament,
                plot=plot,
                output=output_dir
                )
            time_list[idx_outlier].append(time.time() - start)

            start = time.time()
            mean_array = calculations.calculate_mean_prior(
                input_array=filament[data_rotated_name],
                window_size=window_size,
                inside_tolerance_idx=inside_tol_idx,
                outside_tolerance_idx=outside_tol_idx,
                plot=plot,
                output=output_dir
                )
            time_list[idx_mean].append(time.time() - start)

            if plot:
                calculations.plot_polar('mean_array', mean_array, rotate_angle, 180, -180, output=output_dir)

            start = time.time()
            mean_array = calculations.subtract_and_adjust_angles(
                mean_array, -rotate_angle, angle_max, angle_min
                )
            time_list[idx_sub_2].append(time.time() - start)

            if plot:
                calculations.plot_polar('mean_array', mean_array, 0, angle_max, angle_min, output=output_dir)

            start = time.time()
            filament = add_column(filament, mean_array, angle_new)
            time_list[idx_add].append(time.time() - start)

            start = time.time()
            if idx == 0:
                new_array = filament
            else:
                new_array = np.append(new_array, filament)
            time_list[idx_add_2].append(time.time() - start)

        for idx, aaa in enumerate(time_list):
            print(idx, sum(aaa), sum(aaa)/float(len(aaa)))

        array = add_column(array, new_array[angle_new], angle_new)
        if typ == 'sphire':
            array = swap_columns(array, angle, angle_new)
        else:
            pass

    # Sort the array back to the original order
    array = np.sort(array, order=array_order)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if typ == 'relion':
        header_string = write_star.create_header_string(output_names)
        write_star.write_star_file(array[output_names], header_string, '{0}/TEST.star'.format(output_dir))
    elif typ == 'sphire':
        write_sphire.write_params_file(array, output_names, '{0}/{1}.txt'.format(output_dir, params))
    else:
        pass


if __name__ == '__main__':
    plot = False
    if sys.argv[1] == 'relion':
        name = 'data_test2.star'
        typ = 'relion'
        plot = True
    else:
        plot = True
        #name = 'bdb:../Particles/stack_dw'
        name = 'bdb:stack'
        typ = 'sphire'

    index='index.txt'
    params='params.txt'
    #index='../REFINE_CREATE_REF/main001/chunk_0_001.txt'
    #params='../REFINE_CREATE_REF/main001/params-chunk_0_001.txt'
    tolerance = 30
    tolerance_filament = 0.2
    window_size = 3
    output='juhuuuu'

    main(
        file_name=name,
        tolerance_psi=tolerance,
        tolerance_theta=tolerance/2,
        tolerance_filament=tolerance_filament,
        window_size=window_size,
        typ=typ,
        plot=plot,
        index=index,
        params=params,
        output_dir=output
        )
