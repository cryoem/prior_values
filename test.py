import sparx as sp
import numpy as np


stack = 'bdb:stack'

dict_list = []
dummy = sp.EMData()
idx = 0
while True:
    try:
        dummy.read_image(stack, idx, True)
        dict_list.append(dummy.get_attr_dict())
    except Exception:
        break
    idx += 1

#Determine dtype
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

array = np.empty(len(dict_list), dtype=dtype_list)

for idx, entry in enumerate(dict_list):
    for key in entry:
        array[idx][key] = entry[key]

print(len(array))
