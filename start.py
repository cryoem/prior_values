#!/usr/bin/env python
import sys
sys.path.append('modules')
sys.path.append('/work1/home/stabrin/Jasp_cLys_ADP/prior_values/modules')
import numpy as np
import numpy.lib.recfunctions as nlr
import os as os
import time
import calculations
import read_sphire
import read_star
import write_star
import write_sphire


def combine_arrays(array_list):
    """Add column to input array"""
    dtype_new = []
    for entry in array_list:
        assert(len(entry) == len(array_list[0]))
        dtype_new += entry.dtype.descr
    array_combined = np.empty(len(array_list[0]), dtype=dtype_new)

    for entry in array_list:
        for name in entry.dtype.names:
            array_combined[name] = entry[name]

    return array_combined


def create_substack(array, indices):
    """Create a substack of an array"""
    new_array = array[indices]
    return new_array


def import_stack(stack, params=None, index=None, typ='sphire'):
    """Import the original stack and create a substack"""
    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0

        if isinstance(stack, basestring):
            original_stack = read_sphire.get_sphire_stack(stack)
        else:
            original_stack = stack
        parameter = read_sphire.get_sphire_file('params', params)
        indices = read_sphire.get_sphire_file('index', index)

        substack = create_substack(original_stack, indices)
        array = combine_arrays([substack, parameter])

        stack_id = 'source_n'
        mic_name, filament_name, particle_id = \
            original_stack.dtype.names

        angle_name = [
            ['psi', 'psi_prior', 'psi_rot'],
            ['theta', 'theta_prior', 'theta_rot']
            ]

        output_names = list(parameter.dtype.names)
        del original_stack, parameter, indices

    elif typ == 'relion':
        angle_max = 180
        angle_min = -180

        array, header, path = read_star.import_star_file(stack)

        stack_id = 'source_n'
        filament_name = '_rlnHelicalTubeID'
        mic_name = '_rlnMicrographName'
        particle_id = '_rlnImageName'
        angle_name = [
            ['_rlnAnglePsi', '_rlnAnglePsiPrior', '_rlnAnglePsiRotated'],
            ['_rlnAngleTilt', '_rlnAngleTiltPrior', '_rlnAngleTiltRotated']
            ]

        output_names = list(array.dtype.names)
        array_stack_id = np.empty(len(array), dtype=[(stack_id, '<i8')])
        array_stack_id[stack_id] = np.arange(len(array))
        array = combine_arrays([array, array_stack_id])

    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    return [array, stack_id, mic_name, filament_name, particle_id, angle_name, output_names, angle_max, angle_min]


def main(file_name, data, tolerance_psi, tolerance_theta, tolerance_filament, window_size, plot=False, typ='sphire', output_dir=None, params=None):
    """Start calculation"""

    # Extract data
    array, stack_id, mic_name, filament_name, particle_id, angle_name, output_names, angle_max, angle_min = data

    if output_dir is None:
        output_dir = '.'

    if plot:
        do_plot = True
    else:
        do_plot = False

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
    for name in array.dtype.names:
        array_temp[name] = array[name]
    for angle in angle_name:
        array_temp[angle[IDX_ROT]] = np.copy(array[angle[IDX_OLD]])

    # Sort the array and remove array_temp from scope
    array = np.sort(array_temp, order=[mic_name, filament_name, particle_id])
    del array_temp

    # Split the array into filaments
    filament_array = calculations.get_filaments(array=array, filament_name=filament_name)

    # Loop over both angles and their tolerance
    for angle, tolerance in zip(angle_name, [tolerance_psi, tolerance_theta]):
        # Array names
        angle_old = angle[IDX_OLD]
        angle_prior = angle[IDX_NEW]
        angle_rot = angle[IDX_ROT]
        print(angle_old)

        # Loop over all filaments
        for idx, filament in enumerate(filament_array):
            # Do plot if necessary
            if do_plot:
                if idx % 1000 == 0:
                    plot = True
                else:
                    plot = False
            if plot:
                calculations.plot_polar('raw_data', filament[angle_rot], 0, angle_max, 0, output=output_dir)

            # Shift the angle range from 180 to -180
            calculations.subtract_and_adjust_angles(filament[angle_rot], 0, 180, -180)

            # Rotate the angle range, so that the median is the new center
            rotate_angle = calculations.rotate_angles(filament[angle_rot], plot, output=output_dir)

            # Calculate the indices of outliers
            is_outlier, rotate_angle, inside_tol_idx, outside_tol_idx = calculations.get_filament_outliers(
                data_rotated=filament[angle_rot],
                rotate_angle=rotate_angle,
                tolerance=tolerance,
                tolerance_filament=tolerance_filament,
                plot=plot,
                output=output_dir
                )

            # Calculate the new prior values
            calculations.calculate_mean_prior(
                input_array=filament[angle_rot],
                mean_array=filament[angle_prior],
                window_size=window_size,
                inside_tolerance_idx=inside_tol_idx,
                outside_tolerance_idx=outside_tol_idx,
                plot=plot,
                output=output_dir
                )

            if plot:
                calculations.plot_polar('mean_array', filament[angle_prior], rotate_angle, 180, -180, output=output_dir)

            # Adjust the angles to match the aimed angle range
            calculations.subtract_and_adjust_angles(
                filament[angle_prior], -rotate_angle, angle_max, angle_min
                )

            if plot:
                calculations.plot_polar('mean_array', filament[angle_prior], 0, angle_max, angle_min, output=output_dir)

    # Combine the filaments to one array
    array_out = np.empty(len(array), dtype=array.dtype.descr)
    index = 0
    for entry in filament_array:
        for row in entry:
            array_out[index] = row
            index += 1

    # Sort the array back to the original order
    array_out = np.sort(array_out, order=stack_id)

    # Write output
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if typ == 'relion':
        header_string = write_star.create_header_string(output_names)
        write_star.write_star_file(array_out[output_names], header_string, '{0}_prior.star'.format(file_name.split('.star')[0]))
    elif typ == 'sphire':
        write_sphire.write_params_file(array_out, output_names, '{0}_prior.txt'.format(params.split('.txt')[0]))
    else:
        assert(False)


if __name__ == '__main__':
    plot = False
    if sys.argv[1] == 'relion':
        name = 'data_test.star'
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

    data = import_stack(stack=name, index=index, params=params, typ=typ)

    main(
        file_name=name,
        data=data,
        tolerance_psi=tolerance,
        tolerance_theta=tolerance/2,
        tolerance_filament=tolerance_filament,
        window_size=window_size,
        typ=typ,
        plot=plot,
        output_dir=output,
        params=params
        )
