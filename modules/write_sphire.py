def write_params_file(array, names, file_name):
    """Write sphire parameter file"""
    with open(file_name, 'w') as f:
        for element in array:
            for name in names:
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
