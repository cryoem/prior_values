import numpy as np


def create_header_string(header_names):
    """Create and return the header string"""
    header_string = ['\ndata_\n\nloop_\n']
    for idx, entry in enumerate(header_names):
        header_string.append('{0} #{1}\n'.format(entry, idx+1))

    return ''.join(header_string)


def write_star_file(output_array, header_string, output_file):
    """Write an output star file"""
    written_string = []

    # Delete nans
    return_array = np.empty(0, dtype=output_array.dtype.descr)
    for row in output_array:
        if np.isnan(row['_rlnAnglePsiPrior']):
            continue
        if np.isnan(row['_rlnAngleTiltPrior']):
            continue
        else:
            return_array = np.append(return_array, row)

    # Write output
    with open('{0}'.format(output_file), 'w') as f:
        f.write(header_string)

        for row in return_array:
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
                written_string.append(text)
            f.write('\n')
            written_string.append('\n')

    return ''.join(written_string), return_array
