import sparx as sp
import numpy as np


def get_sphire_stack(stack_path):
    """Import the sphire bdb stack to numpy array"""
    image_data = sp.EMData()
    dict_list = []
    idx = 0
    while True:
        try:
            image_data.read_image(stack_path, idx, True)
            dict_list.append(image_data.get_attr_dict())
        except Exception:
            break
        idx += 1

    dtype_list = []
    for key in dict_list[0]:
        if isinstance(dict_list[0][key], int):
            dtype_list.append((key, '<i8'))
        elif isinstance(dict_list[0][key], float):
            dtype_list.append((key, '<f8'))
        elif isinstance(dict_list[0][key], list):
            dtype_list.append((key, 'O'))
        elif isinstance(dict_list[0][key], dict):
            dtype_list.append((key, 'O'))
        elif isinstance(dict_list[0][key], basestring):
            dtype_list.append((key, '|S200'))
        else:
            dtype_list.append((key, 'O'))

    data_array = np.empty(len(dict_list), dtype=dtype_list)

    for idx, entry in enumerate(dict_list):
        for key in entry:
            data_array[idx][key] = entry[key]

    return data_array


def get_sphire_file(typ, input_file):
    """Import the params and index file"""

    if typ == 'index':
        dtype = int
    elif typ == 'params':
        dtype = [('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'), ('err2', '<f8'), ('norm', '<f8')]
    else:
        assert(False)

    data = np.genfromtxt(input_file, dtype=dtype)

    return data
