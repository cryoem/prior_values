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


