import sparx as sp
import numpy as np
import shutil


def get_stack_dtype():
    """Return the dtype of the sphire stack array"""
    dtype_list = [
        ('ptcl_source_image', '|S200'),
        ('filament', '|S200'),
        ('data_n', '<i8')
        ]
    return dtype_list


def import_sphire_stack(stack_path):
    """Import the necessary data from a bdb/hdf stack"""
    dtype_list = get_stack_dtype()

    imported_data = []
    for name, typ in dtype_list:
        data = sp.EMUtil.get_all_attributes(stack_path, name)
        imported_data.append(data)

    data_array = np.empty(len(imported_data[0]), dtype=dtype_list)
    for idx, dtype in enumerate(dtype_list):
        data_array[dtype[0]] = imported_data[idx]

    return data_array


def import_sphire_params(input_file):
    """Import the params and index file"""

    dtype_import = [('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'), ('err2', '<f8'), ('norm', '<f8')]
    dtype = dtype_import + [('source_n', '<i8')]

    data_import = np.genfromtxt(input_file, dtype=dtype_import)

    data = np.empty(len(data_import), dtype=dtype)
    data['source_n'] = np.arange(len(data))
    for name in data_import.dtype.names:
        data[name] = data_import[name]

    return data


def import_sphire_index(input_file):
    """Import the params and index file"""

    dtype = [('stack_idx', '<i8')]
    data = np.genfromtxt(input_file, dtype=dtype)

    return data


def write_params_file(array, names, file_name, file_name_old, prior_tracker):
    """Write sphire parameter file"""
    new_name_order = [
        'phi',
        'shift_x',
        'shift_y',
        'err1',
        'err2',
        'norm'
        ]
    for angle in prior_tracker['angle_names'][::-1]:
        new_name_order.insert(1, angle[prior_tracker['idx_angle_prior']])
    if prior_tracker['tracker']['state'] == 'RESTRICTED':
        shutil.move(file_name_old, file_name)
    else:
        file_name_old = '{0}_not_applied.txt'.format(file_mame)
    with open(file_name_old, 'w') as f:
        for element in array:
            if element[prior_tracker['outlier']]:
                continue
            else:
                pass
            for name in new_name_order:
                if isinstance(element[name], float):
                    text = '{:> 15.6f}'.format(element[name])
                if isinstance(element[name], int):
                    text = '{:> 7d}'.format(element[name])
                if isinstance(element[name], basestring):
                    text = '{:>{}s}'.format(
                        element[name], len(element[name]) + 6
                        )
                f.write(text)
            f.write('\n')


def write_index_file(array, file_name, file_name_old, prior_tracker):
    """Write sphire index file"""
    if prior_tracker['tracker']['state'] == 'RESTRICTED':
        shutil.move(file_name_old, file_name)
    else:
        file_name_old = '{0}_not_applied.txt'.format(file_mame)
    with open(file_name_old, 'w') as f:
        for element in array:
            if element[prior_tracker['outlier']]:
                continue
            else:
                pass
            for name in ['stack_idx']:
                if isinstance(element[name], float):
                    text = '{:> 15.6f}'.format(element[name])
                if isinstance(element[name], int):
                    text = '{:> 7d}'.format(element[name])
                if isinstance(element[name], basestring):
                    text = '{:>{}s}'.format(
                        element[name], len(element[name]) + 6
                        )
                f.write(text)
            f.write('\n')

