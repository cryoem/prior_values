import sys
sys.path.append('modules')
sys.path.append('.')
import os as os
import sparx as sp
import numpy as np
import write_star


class TestWriteStar():
    def test_create_header_string_is_string(self):
        header_names = [
            '_rlnCoordinateX',
            '_rlnCoordinateY',
            '_rlnHelicalTubeID',
            '_rlnHelicalTrackLength'
            ]
        header_string = write_star.create_header_string(header_names)
        assert(isinstance(header_string, basestring))


    def test_create_header_string_has_newline(self):
        header_names = [
            '_rlnCoordinateX',
            '_rlnCoordinateY',
            '_rlnHelicalTubeID',
            '_rlnHelicalTrackLength'
            ]
        header_string = write_star.create_header_string(header_names)
        assert(header_string[-1] == '\n')


    def test_create_header_string_check_content_name(self):
        header_names = [
            '_rlnCoordinateX',
            '_rlnCoordinateY',
            '_rlnHelicalTubeID',
            '_rlnHelicalTrackLength'
            ]
        header_string = write_star.create_header_string(header_names)
        for idx, entry in enumerate(header_names):
            assert(entry in header_string)


    def test_create_header_string_check_content_number(self):
        header_names = [
            '_rlnCoordinateX',
            '_rlnCoordinateY',
            '_rlnHelicalTubeID',
            '_rlnHelicalTrackLength'
            ]
        header_string = write_star.create_header_string(header_names)
        for idx, entry in enumerate(header_names):
            assert(str(idx+1) in header_string)


    def test_write_star_file_exists(self):
        output_file = 'test_output.star'
        output_array = np.array(
            [
                (0, '0', 0.0, np.nan, 0.0),
                (1, '1', 1.0, np.nan, 1.0),
                (2, '2', 2.0, np.nan, 2.0),
                (3, '3', 3.0, np.nan, 3.0),
                (0, '0', 0.0, 0.0, 0.0),
                (1, '1', 1.0, 1.0, 1.0),
                (2, '2', 2.0, 2.0, 2.0),
                (3, '3', 3.0, 3.0, 3.0),
                (0, '0', 0.0, 0, np.nan),
                (1, '1', 1.0, 1, np.nan),
                (2, '2', 2.0, 2, np.nan),
                (3, '3', 3.0, 3, np.nan)
            ],
            dtype=[
                ('int', '<i8'),
                ('str', '|S100'),
                ('float', '<f8'),
                ('_rlnAnglePsiPrior', '<f8'),
                ('_rlnAngleTiltPrior', '<f8')
                ]
            )
        header_string = '\ndata_\n\nloop_\nint #1\nstr #2\nfloat #3\n_rlnAnglePsiPrior #4\n_rlnAngleTiltPrior #5\n'
        return_string, return_array = write_star.write_star_file(
            output_array=output_array,
            header_string=header_string,
            output_file=output_file
            )
        assert(os.path.exists(output_file))
        os.remove(output_file)


    def test_write_star_file_no_nans(self):
        output_file = 'test_output.star'
        output_array = np.array(
            [
                (0, '0', 0.0, np.nan, 0.0),
                (1, '1', 1.0, np.nan, 1.0),
                (2, '2', 2.0, np.nan, 2.0),
                (3, '3', 3.0, np.nan, 3.0),
                (0, '0', 0.0, 0.0, 0.0),
                (1, '1', 1.0, 1.0, 1.0),
                (2, '2', 2.0, 2.0, 2.0),
                (3, '3', 3.0, 3.0, 3.0),
                (0, '0', 0.0, 0, np.nan),
                (1, '1', 1.0, 1, np.nan),
                (2, '2', 2.0, 2, np.nan),
                (3, '3', 3.0, 3, np.nan)
            ],
            dtype=[
                ('int', '<i8'),
                ('str', '|S100'),
                ('float', '<f8'),
                ('_rlnAnglePsiPrior', '<f8'),
                ('_rlnAngleTiltPrior', '<f8')
                ]
            )
        header_string = '\ndata_\n\nloop_\nint #1\nstr #2\nfloat #3\n_rlnAnglePsiPrior #4\n_rlnAngleTiltPrior #5\n'
        return_string, return_array = write_star.write_star_file(
            output_array=output_array,
            header_string=header_string,
            output_file=output_file
            )
        assert(' nan' not in return_string)
        os.remove(output_file)


    def test_write_star_file_len_4(self):
        output_file = 'test_output.star'
        output_array = np.array(
            [
                (0, '0', 0.0, np.nan, 0.0),
                (1, '1', 1.0, np.nan, 1.0),
                (2, '2', 2.0, np.nan, 2.0),
                (3, '3', 3.0, np.nan, 3.0),
                (0, '0', 0.0, 0.0, 0.0),
                (1, '1', 1.0, 1.0, 1.0),
                (2, '2', 2.0, 2.0, 2.0),
                (3, '3', 3.0, 3.0, 3.0),
                (0, '0', 0.0, 0, np.nan),
                (1, '1', 1.0, 1, np.nan),
                (2, '2', 2.0, 2, np.nan),
                (3, '3', 3.0, 3, np.nan)
            ],
            dtype=[
                ('int', '<i8'),
                ('str', '|S100'),
                ('float', '<f8'),
                ('_rlnAnglePsiPrior', '<f8'),
                ('_rlnAngleTiltPrior', '<f8')
                ]
            )
        header_string = '\ndata_\n\nloop_\nint #1\nstr #2\nfloat #3\n_rlnAnglePsiPrior #4\n_rlnAngleTiltPrior #5\n'
        return_string, return_array = write_star.write_star_file(
            output_array=output_array,
            header_string=header_string,
            output_file=output_file
            )
        assert(len(return_array) == 4)
        os.remove(output_file)



