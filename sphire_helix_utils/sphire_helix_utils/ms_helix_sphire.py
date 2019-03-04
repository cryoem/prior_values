import sparx as sp
import numpy as np
import shutil


def import_sphire_stack(stack_path, has_class_id):
    """Import the necessary data from a bdb/hdf stack"""
    dtype_list = [('ptcl_source_image', '|S200'), ('filament', '|S200'), ('data_n', '<i8')] if has_class_id is False \
        else [('ptcl_source_image', '|S200'), ('filament', '|S200'), ('data_n', '<i8'), ('ISAC_class_id', '<i8')]

    imported_data = []
    is_filament = True
    for name, typ in dtype_list:
        try:
            data = sp.EMUtil.get_all_attributes(stack_path, name)
            imported_data.append(data)
        except KeyError:
            if name == 'filament':
                dtype_list.extend([('filament_id', '|S200'),('segment_id', '<i8')])
                is_filament = False
            else:
                print (" ERROR: the type '"+name+"' is not present")
                exit(-1)

    if is_filament is False:
        dtype_list.remove(('filament', '|S200'))

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

    output_name = prepare_output(
        tracker=prior_tracker['tracker'],
        file_name=file_name,
        file_name_old=file_name_old
        )
    write_file(output_name=output_name, array=array, name_list=new_name_order, outlier_apply=prior_tracker['do_discard_outlier'], outlier_name=prior_tracker['outlier'])


def write_index_file(array, file_name, file_name_old, prior_tracker):
    """Write sphire index file"""

    output_name = prepare_output(
        tracker=prior_tracker['tracker'],
        file_name=file_name,
        file_name_old=file_name_old
        )
    write_file(output_name=output_name, array=array, name_list=['stack_idx'], outlier_apply=prior_tracker['do_discard_outlier'], outlier_name=prior_tracker['outlier'])

def write_file(output_name, array, name_list, outlier_apply, outlier_name):
    with open(output_name, 'w') as f:
        for element in array:
            if element[outlier_name] == 1:
                if outlier_apply:
                    continue
                else:
                    pass
            else:
                pass
            for name in name_list:
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


def prepare_output(tracker, file_name, file_name_old):
    default_name = '{0}_not_applied.txt'.format(file_name)

    if isinstance(tracker, basestring):
        output_name = default_name
    elif isinstance(tracker, dict):
        if tracker['constants']['apply_prior']:
            if tracker['state'] == 'RESTRICTED' or tracker['state'] == 'FINAL':
                shutil.move(file_name_old, file_name)
                output_name = file_name_old
            else:
                output_name = default_name

        else:
            output_name = default_name
    else:
        print('Tracker instance "{0}" not known!'.format(type(tracker)))
        assert(False)

    return output_name
