import sparx as sp
import numpy as np


def get_sphire_stack(stack_path):
    """Import the sphire bdb stack to numpy array"""
    dtype_list = [
        ('ptcl_source_image', '|S200'),
        ('filament', '|S200'),
        ('data_n', '<i8')
        ]

    imported_data = []
    for name, typ in dtype_list:
        data = sp.EMUtil.get_all_attributes(stack_path, name)
        imported_data.append(data)

    data_array = np.empty(len(imported_data[0]), dtype=dtype_list)
    for idx, dtype in enumerate(dtype_list):
        data_array[dtype[0]] = imported_data[idx]

    return data_array


def get_sphire_file(typ, input_file):
    """Import the params and index file"""

    if typ == 'index':
        dtype = int
        data = np.genfromtxt(input_file, dtype=dtype)

    elif typ == 'params':
        dtype_import = [('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'), ('err2', '<f8'), ('norm', '<f8')]
        dtype = dtype_import + [('source_n', '<i8')]

        data_import = np.genfromtxt(input_file, dtype=dtype_import)

        data = np.empty(len(data_import), dtype=dtype)
        data['source_n'] = np.arange(len(data))
        for name in data_import.dtype.names:
            data[name] = data_import[name]

    else:
        assert(False)

    return data
