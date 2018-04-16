import sys
sys.path.append('modules')
sys.path.append('.')
import os as os
import sparx as sp
import numpy as np
import start


class TestStart():
    class TestMain():
        def test_main_return_none_sphire(self):
            """Test if the main function is running successfull"""
            name = 'bdb:stack_small'
            tolerance = 30
            tolerance_filament = 0.25
            window_size = 4
            typ = 'sphire'
            start.main(
                file_name=name,
                tolerance=tolerance,
                tolerance_filament=tolerance_filament,
                window_size=window_size,
                typ=typ
                )
            assert(True)

        def test_main_return_none_relion(self):
            """Test if the main function is running successfull"""
            name = 'data_test.star'
            tolerance = 30
            tolerance_filament = 0.25
            window_size = 4
            typ = 'relion'
            start.main(
                file_name=name,
                tolerance=tolerance,
                tolerance_filament=tolerance_filament,
                window_size=window_size,
                typ=typ
                )
            assert(True)

        def test_main_unknown_typ(self):
            """Test if the main function is running successfull"""
            name = 'data_test.star'
            tolerance = 30
            tolerance_filament = 0.25
            window_size = 4
            typ = 'ok'
            return_value = start.main(
                file_name=name,
                tolerance=tolerance,
                tolerance_filament=tolerance_filament,
                window_size=window_size,
                typ=typ
                )
            assert(return_value == 'Unreachable code!')

    class TestAddColumn():
        def test_add_column(self):
            arr1 = np.array(
                [
                    (0, '0', 0.0),
                    (0, '1', 1.0),
                    (1, '2', 2.0)
                ],
                dtype=[
                    ('_rlnHelicalTubeID', '<i8'),
                    ('str', '|S100'),
                    ('float', '<f8')
                    ]
                )
            arr2 = np.array([2, 3, 4])
            return_array = start.add_column(arr1, arr2, 'test')
            assert(np.array_equal(arr2, return_array['test']))

    class TestSwapColumns():
        def test_swap_column_1(self):
            arr1 = np.array(
                [
                    (0, 4., 0.0),
                    (0, 5., 1.0),
                    (1, 6., 2.0)
                ],
                dtype=[
                    ('_rlnHelicalTubeID', '<i8'),
                    ('str', '<f8'),
                    ('float', '<f8')
                    ]
                )
            return_array = start.swap_columns(arr1, 'str', 'float')
            print(arr1)
            print(return_array)
            assert(np.array_equal(arr1['str'], return_array['float']))

        def test_swap_column_2(self):
            arr1 = np.array(
                [
                    (0, 4., 0.0),
                    (0, 5., 1.0),
                    (1, 6., 2.0)
                ],
                dtype=[
                    ('_rlnHelicalTubeID', '<i8'),
                    ('str', '<f8'),
                    ('float', '<f8')
                    ]
                )
            return_array = start.swap_columns(arr1, 'str', 'float')
            print(arr1)
            print(return_array)
            assert(np.array_equal(arr1['float'], return_array['str']))

