import sys
sys.path.append('modules')
sys.path.append('/work1/home/stabrin/Jasp_cLys_ADP/prior_values/modules')
import numpy as np
import os as os
import time
import calculations
import read_sphire
import read_star
import write_star
import write_sphire


def combine_arrays(array_one, array_two):
    """Add column to input array"""
    assert(len(array_one) == len(array_two))
    dtype_one = array_one.dtype.descr
    dtype_two = array_two.dtype.descr
    dtype_new = dtype_one + dtype_two
    array_combined = np.empty(len(array_one), dtype=dtype_new)

    for name in array_one.dtype.names:
        array_combined[name] = np.copy(array_one[name])
    for name in array_two.dtype.names:
        array_combined[name] = np.copy(array_two[name])
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

def create_substack_new(array, indices):
    """Create a substack of an array"""
    new_array = array[indices]
    return new_array

def main(file_name, tolerance_psi, tolerance_theta, tolerance_filament, window_size, plot=False, typ='sphire', params=None, index=None, output_dir=None):
    """Start calculation"""

    if output_dir is None:
        output_dir = '.'

    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0

        start = time.time()
        parameter = read_sphire.get_sphire_file('params', params)
        indices = read_sphire.get_sphire_file('index', index)
        print('import small', time.time()-start)

        start = time.time()
        original_stack = read_sphire.get_sphire_stack(file_name)
        print('import', time.time()-start)
        start = time.time()
        substack = create_substack(original_stack, indices)
        print('substack', time.time()-start)
        start = time.time()
        array = combine_arrays(substack, parameter)
        print('combine', time.time()-start)

        start = time.time()
        original_stack_new = read_sphire.get_sphire_stack_new(file_name)
        print('import new', time.time()-start)
        start = time.time()
        substack_new = create_substack_new(original_stack_new, indices)
        print('substack new', time.time()-start)
        start = time.time()
        array_new = combine_arrays(substack_new, parameter)
        print('combine new', time.time()-start)

        id_name = 'filament'
        particle_name = 'data_n'
        micrograph_name = 'ptcl_source_image'
        angle_name = ['psi', 'theta']
        angle_name_new = ['psi_prior', 'theta_prior']

        output_names = list(parameter.dtype.names)

        for array in [array, array_new]:
            print('SPEED GO!')
            start = time.time()
            array = np.sort(array, order=[micrograph_name, id_name, particle_name])
            print('sort', time.time() - start, len(array), len(array[0]))
            start = time.time()
            filament_array = calculations.get_filaments(array, id_name)
            print('original', time.time() - start, len(filament_array), len(filament_array[0]))

            for entry in ['str', 'int']:
                for idx in range(4):
                    start = time.time()
                    filament_array = calculations.get_filaments_where(array, id_name, entry, idx)
                    print(entry, idx, time.time() - start, len(filament_array), len(filament_array[0]))

        return

    elif typ == 'relion':
        angle_max = 180
        angle_min = -180

        array, header, path = read_star.import_star_file(file_name)

        id_name = '_rlnHelicalTubeID'
        micrograph_name = '_rlnMicrographName'
        particle_name = '_rlnImageName'
        angle_name = ['_rlnAnglePsi', '_rlnAngleTilt']
        angle_name_new = ['_rlnAnglePsiPrior', '_rlnAngleTiltPrior']

        output_names = list(array.dtype.names) + angle_name_new

    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    # Add the particle number to the array
    array_order = 'particle_order'
    order_numbers = np.arange(len(array))
    array = add_column(array, order_numbers, array_order)
    # Sort the array
    array = np.sort(array, order=[micrograph_name, id_name, particle_name])

    for angle in angle_name:
        # Add rotated data column to the array
        data_rotated_name = 'data_rotated_{0}'.format(angle)
        array = add_column(array, array[angle], data_rotated_name)

    start = time.time()
    filament_array = calculations.get_filaments(array, id_name)
    print('original', time.time() - start, len(filament_array), len(filament_array[0]))
 
    for entry in ['str', 'int']:
        for idx in range(4):
            start = time.time()
            filament_array = calculations.get_filaments_where(array, id_name, entry, idx)
            print(entry, idx, time.time() - start, len(filament_array), len(filament_array[0]))

    array_modified = None
    if plot:
        do_plot = True
    else:
        do_plot = False

    idx_sub = 0
    idx_rotate = 1
    idx_outlier = 2
    idx_mean = 3
    idx_sub_2 = 4
    idx_add = 5
    idx_add_2 = 6
    for angle, angle_new, tolerance in zip(angle_name, angle_name_new, [tolerance_psi, tolerance_theta]):
        print(angle)
        time_list = [[] for i in range(7)]
        data_rotated_name = 'data_rotated_{0}'.format(angle)
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
        name = 'bdb:../Particles/stack_dw'
        typ = 'sphire'

    index='../REFINE_CREATE_REF/main001/chunk_0_001.txt'
    params='../REFINE_CREATE_REF/main001/params-chunk_0_001.txt'
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
