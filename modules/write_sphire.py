def write_params_file(array, file_name):
    """Write sphire parameter file"""
    with open(file_name, 'w') as f:
        for row in array:
            for element in row:
                if isinstance(element, float):
                    text = '{:> 15.6f}'.format(element)
                if isinstance(element, int):
                    text = '{:> 7d}'.format(element)
                if isinstance(element, basestring):
                    text = '{:>{}s}'.format(
                        element, len(element) + 6
                        )
                f.write(text)
            f.write('\n')
