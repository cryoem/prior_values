import sys
sys.path.append('modules')
import os as os
import sparx as sp
import numpy as np
import calculations
import read_sphire
import read_star
import write_star

def test_get_filaments_length():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (1, '2', 2.0),
            (1, '3', 3.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 2.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    print(output_array)
    print(return_array)
    assert(len(return_array) == 6)


def test_get_filament_outliers_len_1_is_outlier():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    outlier, mean, idx_ins, idx_outs= calculations.get_filament_outliers(return_array[-1]['float'], 2, 30, 0.25)
    print(outlier)
    assert(not outlier)


def test_get_filament_outliers_len_4_is_outlier():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    outlier, mean, idx_ins, idx_outs= calculations.get_filament_outliers(return_array[0]['float'], 2, 30, 0.25)
    print(outlier)
    assert(outlier)


def test_get_filament_outliers_len_4_outliers():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    outlier, mean, idx_ins, idx_outs= calculations.get_filament_outliers(return_array[0]['float'], 2, 30, 0.25)
    assert(np.array_equal(idx_outs, np.array([3], dtype=int)))


def test_get_filament_outliers_len_1_outliers():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array[-1]['float'], 2, 30, 0.25)
    print(idx_outs)
    assert(np.array_equal(idx_outs, np.array([], dtype=int)))


def test_get_filament_outliers_len_4_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array, mean = calculations.rotate_angles(return_array[0]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array, mean, 30, 0.25)
    assert(np.round(mean, 4) == 1.3333)


def test_get_filament_outliers_len_1_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array, mean = calculations.rotate_angles(return_array[-1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array, mean, 30, 0.25)
    assert(mean == 3)


def test_get_filament_outliers_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '3', 32.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (2, '2', 4.0),
            (2, '3', 3.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (2, '2', 2.0),
            (3, '3', 3.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array, mean = calculations.rotate_angles(return_array[-1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array, mean, 30, 0.25)
    assert(mean == 3)


def test_rotate_angles_zero_rotate_angle_odd_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-2, -1, 0, 1, 2, 3, 4], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == 1)


def test_rotate_angles_zero_rotate_angle_odd_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-4, -3, -2, -1, 0, 1, 2], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == -1)


def test_rotate_angles_zero_rotate_angle_even_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-2, -1, 0, 1, 2, 3], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == 0.5)


def test_rotate_angles_zero_rotate_angle_even_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-3, -2, -1, 0, 1, 2], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == -0.5)


def test_rotate_angles_zero_odd_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-4, -3, -2, -1, 0, 1, 2], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-3, -2, -1, 0, 1, 2, 3], dtype=float)))


def test_rotate_angles_zero_odd_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-2, -1, 0, 1, 2, 3, 4], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-3, -2, -1, 0, 1, 2, 3], dtype=float)))


def test_rotate_angles_zero_even_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-2, -1, 0, 1, 2, 3], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5], dtype=float)))


def test_rotate_angles_zero_even_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-3, -2, -1, 0, 1, 2], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5], dtype=float)))


def test_rotate_angles_180_rotate_angle_odd_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-178, -179, 180, 179, 178, 177, 176], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == 179)


def test_rotate_angles_180_rotate_angle_odd_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-176, -177, -178, -179, 180, 179, 178], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == -179.00000000000003)


def test_rotate_angles_180_rotate_angle_even_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-178, -179, 180, 179, 178, 177], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == 179.5)


def test_rotate_angles_180_rotate_angle_even_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-177, -178, -179, 180, 179, 178], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(rotate_angle == -179.5)


def test_rotate_angles_180_odd_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-178, -179, 180, 179, 178, 177, 176], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([3, 2, 1, 0, -1, -2, -3], dtype=float)))


def test_rotate_angles_180_odd_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-176, -177, -178, -179, 180, 179, 178], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([3, 2, 1, 0, -1, -2, -3], dtype=float)))


def test_rotate_angles_180_even_right():
    """Test the rotation of the center of angles"""
    output_array = np.array([-178, -179, 180, 179, 178, 177], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([2.5, 1.5, 0.5, -0.5, -1.5, -2.5], dtype=float)))


def test_rotate_angles_180_even_left():
    """Test the rotation of the center of angles"""
    output_array = np.array([-177, -178, -179, 180, 179, 178], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([2.5, 1.5, 0.5, -0.5, -1.5, -2.5], dtype=float)))


def test_rotate_angle_not_converge_initialy_odd():
    """Test the rotation of the center of angles with random numbers"""
    output_array = np.array([-88, -102, -75, 141, -160, -35, 37, 44, -45, -6, 59], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-43., -57., -30., -174., -115., 10., 82., 89., 0., 39., 104.], dtype=float)))


def test_rotate_angle_not_converge_initialy_even():
    """Test the rotation of the center of angles with random numbers"""
    output_array = np.array([-88, -102, -75, 141, -160, -35, 37, 44, -45, -6], dtype=float)
    return_array, rotate_angle = calculations.rotate_angles(output_array)
    print(output_array)
    print(return_array)
    assert(np.array_equal(return_array, np.array([-28., -42., -15., -159., -100., 25., 97., 104., 15., 54.])))


def test_get_local_mean_180_is_mean():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', -2.0),
            (1, '2', 8.0),
            (1, '3', -7.0),
            (1, '0', 10.0),
            (1, '1', 19.0),
            (2, '2', 10.0),
            (2, '3', -7.0),
            (0, '0', 0.0),
            (0, '1', 9.0),
            (2, '2', -18.0),
            (3, '3', -17.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 180, 30)
    assert(179.58333333333334 == mean)


def test_get_local_mean_180_nr_outliers():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', -2.0),
            (1, '2', 8.0),
            (1, '3', -7.0),
            (1, '0', 40.0),
            (1, '1', 59.0),
            (2, '2', 60.0),
            (2, '3', -7.0),
            (0, '0', 0.0),
            (0, '1', 9.0),
            (2, '2', -18.0),
            (3, '3', -17.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 180, 30)
    assert(nr_outliers == 3)


def test_get_local_mean_180_return_array():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', -2.0),
            (1, '2', 8.0),
            (1, '3', -7.0),
            (1, '0', 10.0),
            (1, '1', 19.0),
            (2, '2', 10.0),
            (2, '3', -7.0),
            (0, '0', 0.0),
            (0, '1', 9.0),
            (2, '2', -18.0),
            (3, '3', -17.0)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 180, 30)
    compare_array = output_array[data_name] - 0.416666666667
    assert(np.array_equal(np.round(return_array, 8), np.round(compare_array, 8)))


def test_get_local_mean_zero_is_mean():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -1.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 1.5, 30)
    assert(mean == 1.6363636363636362)


def test_get_local_mean_zero_nr_outlier():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -1.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 1.5, 30)
    assert(nr_outliers == 1)


def test_get_local_mean_zero_return_array():
    """Get the mean value"""
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -1.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    return_array, mean, nr_outliers = calculations.get_local_mean(output_array['_rlnAnglePsi'], 1.5, 30)
    compare_array = output_array[data_name] + 0.136363636364
    assert(np.array_equal(np.round(return_array, 8), np.round(compare_array, 8)))


def test_get_tolerance_outliers_length():
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -100.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    inside_tolerance, outside_tolerance = calculations.get_tolerance_outliers(output_array['_rlnAnglePsi'], 30)
    assert(len(inside_tolerance) + len(outside_tolerance) == len(output_array))


def test_get_tolerance_outliers_length_outlier():
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -100.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    inside_tolerance, outside_tolerance = calculations.get_tolerance_outliers(output_array['_rlnAnglePsi'], 30)
    assert(len(outside_tolerance) == 2)


def test_subtract_and_adjust_angles_skalar():
    """Test the subtraction angle method"""
    data_subtracted = calculations.subtract_and_adjust_angles(2, 1)
    print(data_subtracted)
    assert(data_subtracted == 1)


def test_subtract_and_adjust_angles_array():
    """Test the subtraction angle method"""
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_subtracted = calculations.subtract_and_adjust_angles(output_array['_rlnAnglePsi'], 1)
    print(data_subtracted)
    assert(np.array_equal(data_subtracted, np.array([-2.5, -1.5, -0.5], dtype=float)))


def test_find_tolerance_outliers_length():
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -100.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    inside_tolerance, outside_tolerance = calculations.find_tolerance_outliers(output_array['_rlnAnglePsi'], 30)
    print(inside_tolerance)
    print(outside_tolerance)
    assert(len(inside_tolerance) + len(outside_tolerance) == len(output_array))


def test_find_tolerance_outliers_length_outlier():
    output_array = np.array(
        [
            (0, '0', -1.5),
            (0, '1', -0.5),
            (1, '2', 0.5),
            (1, '3', 1.5),
            (1, '0', -100.5),
            (1, '1', -0.5),
            (2, '2', 0.5),
            (2, '3', 1.5),
            (0, '0', -1.5),
            (0, '1', -0.5),
            (2, '2', 0.5),
            (3, '3', 31.5)
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('_rlnAnglePsi', '<f8')
            ]
        )
    data_name = '_rlnAnglePsi'
    inside_tolerance, outside_tolerance = calculations.get_tolerance_outliers(output_array['_rlnAnglePsi'], 30)
    assert(len(outside_tolerance) == 2)


def test_calculate_mean_prior_no_outliers_length():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 5, idx_ins, idx_outs, mean)
    print(mean_array)
    assert(len(mean_array) == 10)


def test_calculate_mean_prior_no_outliers_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 5, idx_ins, idx_outs, mean)
    print(mean_array)
    assert(np.round(mean_array[0], 2) == 1.03)


def test_calculate_mean_prior_one_outlier_length():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 120.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 5, idx_ins, idx_outs, mean)
    print(mean_array)
    assert(len(mean_array) == 10)


def test_calculate_mean_prior_one_outlier_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 120.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 5, idx_ins, idx_outs, mean)
    print(mean_array)
    assert(np.round(mean_array[0], 2) == 1.02)


def test_calculate_mean_prior_small_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[-1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 3, idx_ins, idx_outs, mean)
    assert(mean_array[0] == mean)


def test_calculate_mean_prior_180_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', -177.0),
            (1, '3', -178.0),
            (1, '0', -179.0),
            (1, '0', 180.0),
            (1, '1', 179.0),
            (1, '1', -178.0),
            (0, '0', 180.0),
            (0, '1', -178.0),
            (0, '2', 179.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 3, idx_ins, idx_outs, mean)
    print(mean_array)
    assert(np.round(mean_array[0], 3) == -177.333)


def test_calculate_mean_prior_small_180_mean():
    output_array = np.array(
        [
            (0, '0', 0.0),
            (0, '1', 1.0),
            (0, '2', 1.0),
            (0, '3', 170.0),
            (1, '2', 2.0),
            (1, '2', 2.0),
            (1, '3', 2.0),
            (1, '0', 0.0),
            (1, '0', 0.0),
            (1, '1', 1.0),
            (1, '1', 1.0),
            (0, '0', 180.0),
            (0, '1', -178.0),
            (0, '2', 179.0),
        ],
        dtype=[
            ('_rlnHelicalTubeID', '<i8'),
            ('str', '|S100'),
            ('float', '<f8')
            ]
        )
    return_array = calculations.get_filaments(output_array, '_rlnHelicalTubeID')
    return_array2, mean = calculations.rotate_angles(return_array[-1]['float'])
    outlier, mean, idx_ins, idx_outs = calculations.get_filament_outliers(return_array2, mean, 30, 0.25)
    mean_array = calculations.calculate_mean_prior(return_array2, 3, idx_ins, idx_outs, mean)
    print(mean)
    assert(mean_array[0] == mean)


def test_get_sphire_stack_length():
    """Test if the length of the sphire stack is correct"""
    stack_name = 'bdb:stack_small'
    return_array = read_sphire.get_sphire_stack(stack_name)
    print(len(return_array))
    assert(len(return_array) == 684)


def test_create_dtype_dict():
    dtype_dict = read_star.create_dtype_dict()
    assert(isinstance(dtype_dict, dict))


def test_import_star_file_length_data():
    file_name = 'data_test.star'
    data, header, path = read_star.import_star_file(file_name)
    assert(len(data) == 274)


def test_import_star_file_length_header():
    file_name = 'data_test.star'
    data, header, path = read_star.import_star_file(file_name)
    assert(len(header) == 31)


def test_import_star_file_path():
    file_name = 'data_test.star'
    data, header, path = read_star.import_star_file(file_name)
    assert(file_name == path)


def test_create_header_string_is_string():
    header_names = [
        '_rlnCoordinateX',
        '_rlnCoordinateY',
        '_rlnHelicalTubeID',
        '_rlnHelicalTrackLength'
        ]
    header_string = write_star.create_header_string(header_names)
    assert(isinstance(header_string, basestring))


def test_create_header_string_has_newline():
    header_names = [
        '_rlnCoordinateX',
        '_rlnCoordinateY',
        '_rlnHelicalTubeID',
        '_rlnHelicalTrackLength'
        ]
    header_string = write_star.create_header_string(header_names)
    assert(header_string[-1] == '\n')


def test_create_header_string_check_content_name():
    header_names = [
        '_rlnCoordinateX',
        '_rlnCoordinateY',
        '_rlnHelicalTubeID',
        '_rlnHelicalTrackLength'
        ]
    header_string = write_star.create_header_string(header_names)
    for idx, entry in enumerate(header_names):
        assert(entry in header_string)


def test_create_header_string_check_content_number():
    header_names = [
        '_rlnCoordinateX',
        '_rlnCoordinateY',
        '_rlnHelicalTubeID',
        '_rlnHelicalTrackLength'
        ]
    header_string = write_star.create_header_string(header_names)
    for idx, entry in enumerate(header_names):
        assert(str(idx+1) in header_string)


def test_write_star_file_exists():
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


def test_write_star_file_no_nans():
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


def test_write_star_file_len_4():
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
