import sys
sys.path.append('modules')
import numpy as np
import os as os
import calculations
import read_sphire
import read_star
import write_star
import write_sphire


def wrapped_distribution(array):
    """Calculate a wrapped normal distribution"""
    nr_data = len(array)
    summe = np.sum(np.exp(np.radians(array)*1j))
    complex_mean = summe/float(nr_data)
    complex_angle = np.angle(complex_mean)

    R2 = np.real(complex_mean * np.conj(complex_mean))
    R2_e = (nr_data/float(nr_data-1)) * (R2 - 1/float(nr_data))
    std = np.sqrt(np.log(1/float(R2)))

    mean_list = [np.degrees(complex_angle) for entry in range(nr_data)]
    std_list = [np.degrees(std) for entry in range(nr_data)]

    return mean_list, std_list


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

def main(file_name, tolerance_psi, tolerance_theta, tolerance_filament, window_size, plot=False, typ='sphire', params=None, index=None, output_dir=None):
    """Start calculation"""

    if output_dir is None:
        output_dir = '.'

    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0

        original_stack = read_sphire.get_sphire_stack(file_name)
        parameter = read_sphire.get_sphire_file('params', params)
        indices = read_sphire.get_sphire_file('index', index)
        substack = create_substack(original_stack, indices)
        array = combine_arrays(substack, parameter)

        id_name = 'filament'
        particle_name = 'data_n'
        micrograph_name = 'ptcl_source_image'
        angle_name = ['theta', 'psi']
        angle_name_new = [['theta_prior', 'theta_std'], ['psi_prior', 'psi_std']]

        output_names = list(parameter.dtype.names)
        for entry in angle_name_new:
            output_names += entry

    elif typ == 'relion':
        angle_max = 180
        angle_min = -180

        array, header, path = read_star.import_star_file(file_name)

        id_name = '_rlnHelicalTubeID'
        micrograph_name = '_rlnMicrographName'
        particle_name = '_rlnImageName'
        angle_name = ['_rlnAngleTilt', '_rlnAnglePsi']
        angle_name_new = [['_rlnAngleTiltPrior', '_rlnAngleTiltStd'], ['_rlnAnglePsiPrior', '_rlnAnglePsiStd']]

        output_names = list(array.dtype.names)
        for entry in angle_name_new:
            output_names.append(entry[0])

    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    # Add the particle number to the array and sort it by filament and particle
    order_idx = 'particle_order'
    ordered_numbers = np.arange(len(array))
    array = add_column(array, ordered_numbers, order_idx)
    array = np.sort(array, order=[micrograph_name, id_name, particle_name])

    filament_array = calculations.get_filaments(array, id_name)
    if plot:
        do_plot = True
    else:
        do_plot = False

    for angle, angle_new, tolerance in zip(angle_name, angle_name_new, [tolerance_psi, tolerance_theta]):
        for idx, filament in enumerate(filament_array):
            if do_plot:
                if idx % 1000 == 0:
                    plot = True
                else:
                    plot = False

            mean_list, std_list = wrapped_distribution(filament[angle])
            for name, entry in zip(angle_new, [mean_list, std_list]):
                filament = add_column(filament, entry, name)

            if idx == 0:
                new_array = filament
            else:
                new_array = np.append(new_array, filament)



            if plot:
                calculations.plot_polar('raw_data', filament[angle], 0, angle_max, 0, output=output_dir)
                calculations.plot_polar('mean', filament[angle], 0, angle_max, 0, mean=np.degrees(mean_list[0]), output=output_dir)
                calculations.plot_polar('sigma1', filament[angle], 0, angle_max, 0, mean=np.degrees(mean_list[0]), output=output_dir, tol=np.degrees(std_list[0]))
                calculations.plot_polar('sigma2', filament[angle], 0, angle_max, 0, mean=np.degrees(mean_list[0]), output=output_dir, tol=2*np.degrees(std_list[0]))

        for idx, name in enumerate(angle_new):
            array = add_column(array, new_array[name], name)

    # Sort the array back to the original order
    array = np.sort(array, order=order_idx)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if typ == 'relion':
        header_string = write_star.create_header_string(output_names)
        write_star.write_star_file(array[output_names], header_string, '{0}/TEST.star'.format(output_dir))
    elif typ == 'sphire':
        write_sphire.write_params_file(array, output_names, '{0}/TEST.txt'.format(output_dir))
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
        name = 'bdb:stack_small'
        typ = 'sphire'

    index='index.txt'
    params='params.txt'
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
