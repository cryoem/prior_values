import sparx as sp
import ms_helix_prior
import unittest
from numpy import array as np_array
from numpy import int64 as np_int64
from numpy import float64 as np_float64
from numpy import ndarray, array_equal
from os import remove,path
from subprocess import Popen,PIPE

func_linear = lambda x, a, b: a * x + b
func_dict = { 1: {'func': func_linear, 'params': None}}

def get_list_of_created_file(cmd=["ls *.png"]):
    """ Given a shell command it will give back the string of the console output"""
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    o, e = proc.communicate()
    return o


def clean_up(stuff_to_remove):
    for f in stuff_to_remove:
        if path.exists(f) and path.isfile(f):
            remove(f)


def generate_prior_tracker(apply_method = "std"):
    prior_tracker = dict()
    prior_tracker['array_filament'] = np_array([[ ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 0, 38.32375, 79.75458, 278.43793, 8.00109, 1.00109, 0.19693, 0.73653, 91259.15828, 0, 0, 6.042718322764362e-154, 79.75458, 2314885531238936880, 9.162199477420751e-72, 278.43793, 4051047449742946336, 3467807035425300512), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 1, 35.83593, 55.19391, 350.15674, -1.99891, -3.99891, 0.70511, 0.73476, 91040.31356, 1, 1, 4.948400661721011e+173, 55.19391, 8935143215481254912, 0.0, 350.15674, 8935145457454311936, 3487650908667907), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 2, 39.17223, 77.94179, 48.28169, -7.99891, -2.99891, 0.45521, 0.70617, 87497.71089, 2, 2, 0.0, 77.94179, 5157209670381677, 5.075883983234376e-116, 48.28169, 8317304086824383232, 8313495831334709343), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 3, 33.44401, 80.17834, 187.50038, -2.99891, -7.74279, 0.23672, 0.70772, 87689.01591, 3, 3, 0.0, 80.17834, 7595444411327411305, 7.698438237169649e+218, 187.50038, 1824520799039935077, 113044881408), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 4, 38.73295, 78.84809, 255.00044, 2.00109, 18.00109, 0.21688, 0.74511, 92321.562, 4, 4, 9.076859094468509e+223, 78.84809, 0, 0.0, 255.00044, 0, 0), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 5, 23.93829, 71.0277, 94.21904, -6.99891, 10.00109, 0.48858, 0.72281, 89558.54532, 5, 5, 0.0, 71.0277, 0, 0.0, 94.21904, 7161082258284898662, 6868064479304640884), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 6, 37.77144, 77.47843, 97.96918, -7.99891, -4.99891, 0.4357, 0.70789, 87710.85716, 6, 6, 0.0, 77.47843, 0, 0.0, 97.96918, 0, 0)]], dtype=[('ptcl_source_image', 'S200'), ('filament', 'S200'), ('data_n', '<i8'), ('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'), ('err2', '<f8'), ('norm', '<f8'), ('source_n', '<i8'), ('stack_idx', '<i8'), ('theta_prior', '<f8'), ('theta_rot', '<f8'), ('outlier_theta', '<i8'), ('psi_prior', '<f8'), ('psi_rot', '<f8'), ('outlier_psi', '<i8'), ('outlier', '<i8')])
    prior_tracker['array'] = np_array([ ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 0, 38.32375, 79.75458, 278.43793, 8.00109, 1.00109, 0.19693, 0.73653, 91259.15828, 0, 0, 6.042718322764362e-154, 79.75458, 2314885531238936880, 9.162199477420751e-72, 278.43793, 4051047449742946336, 3467807035425300512), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 1, 35.83593, 55.19391, 350.15674, -1.99891, -3.99891, 0.70511, 0.73476, 91040.31356, 1, 1, 4.948400661721011e+173, 55.19391, 8935143215481254912, 0.0, 350.15674, 8935145457454311936, 3487650908667907), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 2, 39.17223, 77.94179, 48.28169, -7.99891, -2.99891, 0.45521, 0.70617, 87497.71089, 2, 2, 0.0, 77.94179, 5157209670381677, 5.075883983234376e-116, 48.28169, 8317304086824383232, 8313495831334709343), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 3, 33.44401, 80.17834, 187.50038, -2.99891, -7.74279, 0.23672, 0.70772, 87689.01591, 3, 3, 0.0, 80.17834, 7595444411327411305, 7.698438237169649e+218, 187.50038, 1824520799039935077, 113044881408), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 4, 38.73295, 78.84809, 255.00044, 2.00109, 18.00109, 0.21688, 0.74511, 92321.562, 4, 4, 9.076859094468509e+223, 78.84809, 0, 0.0, 255.00044, 0, 0), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 5, 23.93829, 71.0277, 94.21904, -6.99891, 10.00109, 0.48858, 0.72281, 89558.54532, 5, 5, 0.0, 71.0277, 0, 0.0, 94.21904, 7161082258284898662, 6868064479304640884), ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 6, 37.77144, 77.47843, 97.96918, -7.99891, -4.99891, 0.4357, 0.70789, 87710.85716, 6, 6, 0.0, 77.47843, 0, 0.0, 97.96918, 0, 0)], dtype=[('ptcl_source_image', 'S200'), ('filament', 'S200'), ('data_n', '<i8'), ('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'), ('err2', '<f8'), ('norm', '<f8'), ('source_n', '<i8'), ('stack_idx', '<i8'), ('theta_prior', '<f8'), ('theta_rot', '<f8'), ('outlier_theta', '<i8'), ('psi_prior', '<f8'), ('psi_rot', '<f8'), ('outlier_psi', '<i8'), ('outlier', '<i8')])
    prior_tracker['do_discard_outlier'] = False
    prior_tracker['plot'] = False
    prior_tracker['window_size'] = 3
    prior_tracker['angle'] = 'theta'
    prior_tracker['prior_method'] = 'fit'
    prior_tracker['output_file_params'] = 'params'
    prior_tracker['apply_method'] = apply_method
    prior_tracker['plot_lim'] = 4
    prior_tracker['tracker'] = 'bdb:../tests/stack_small'
    prior_tracker['output_dir'] = '.'
    prior_tracker['angle_names'] = [['theta', 'theta_prior', 'theta_rot'], ['psi', 'psi_prior', 'psi_rot']]
    prior_tracker['idx_angle'] = 0
    prior_tracker['tol_filament'] = 0.2
    prior_tracker['angle_prior'] = 'theta_prior'
    prior_tracker['tolerance'] = 15
    prior_tracker['node'] = 0
    prior_tracker['angle_min'] = 0
    prior_tracker['outlier'] = 'outlier'
    prior_tracker['angle_rot'] = 'theta_rot'
    prior_tracker['idx_angle_prior'] = 1
    prior_tracker['output_file_index'] = 'index'
    prior_tracker['angle_max'] = 360
    prior_tracker['output_columns'] = ['phi', 'theta', 'psi', 'shift_x', 'shift_y', 'err1', 'err2', 'norm', 'source_n', 'theta_prior', 'psi_prior']
    prior_tracker['tol_std'] = 1
    prior_tracker['micrograph_id'] = 'ptcl_source_image'
    prior_tracker['segment_id'] = 'data_n'
    prior_tracker['tol_mean'] = 30
    prior_tracker['filament_id'] = 'filament'
    prior_tracker['order'] = 'source_n'
    prior_tracker['idx_angle_rot'] = 2
    prior_tracker['force_outlier'] = True
    return prior_tracker


class Test_wrapped_distribution(unittest.TestCase):
    def test_wrapped_distribution(self):
        m,s=ms_helix_prior.wrapped_distribution(ndarray(shape=(7,), buffer=np_array([ 79.75458,  55.19391,  77.94179 , 80.17834  ,78.84809 , 71.0277,   77.47843]), dtype=float) )
        self.assertTrue( [74.393744681484051, 74.393744681484051, 74.393744681484051, 74.393744681484051, 74.393744681484051, 74.393744681484051, 74.393744681484051] == m)
        self.assertTrue( [8.3077762527065957, 8.3077762527065957, 8.3077762527065957, 8.3077762527065957, 8.3077762527065957, 8.3077762527065957, 8.3077762527065957] == s)



class Test_get_filaments(unittest.TestCase):
    def test_get_filaments(self):
        prior_tracker =generate_prior_tracker()
        prior_tracker_after_get_filament=ms_helix_prior.get_filaments(prior_tracker)
        self.assertTrue(array_equal(prior_tracker['array_filament'] , prior_tracker_after_get_filament['array_filament']))



class Test_get_local_mean(unittest.TestCase):
    def test_get_local_mean(self):
        rotate_angle, nr_outliers = ms_helix_prior.get_local_mean(ndarray(shape=(7,), buffer=np_array([1.81279, -22.74788, 0., 2.23655, 0.9063, -6.91409, -0.46336]), dtype=float), rotate_angle=np_float64(77.94179),tolerance=30)
        self.assertTrue(0 == nr_outliers and 74.34612 ==rotate_angle )


class Test_rotate_angles_median(unittest.TestCase):
    output_dir ='./prior_images_0'
    def test_rotate_angles_median_without_plot_and_with_odd_array(self):
        ar = ndarray(shape=(7,), buffer=np_array([ 79.75458,  55.19391,  77.94179 , 80.17834  ,78.84809 , 71.0277,   77.47843]), dtype=float)
        self.assertTrue(77.94179 == ms_helix_prior.rotate_angles_median(ar, {'do_plot': False, 'output_dir': self.output_dir }))
        clean_up(get_list_of_created_file(cmd=["ls ./*.png"]).split("\n"))

    def test_rotate_angles_median_with_plot_and_with_odd_array(self):
        ar = ndarray(shape=(7,), buffer=np_array([79.75458, 55.19391, 77.94179, 80.17834, 78.84809, 71.0277, 77.47843]), dtype=float)
        self.assertTrue(77.94179 == ms_helix_prior.rotate_angles_median(ar, {'do_plot': True,'output_dir': self.output_dir, 'prefix': 'DEFAULT'}))
        clean_up(get_list_of_created_file(cmd=["ls ./*.png"]).split("\n"))

    def test_rotate_angles_median_without_plot_and_with_even_array(self):
        ar = ndarray(shape=(8,), buffer=np_array([ 79.75458,  55.19391,  77.94179 , 80.17834  ,78.84809 , 71.0277,   77.47843, 77.8888]), dtype=float)
        self.assertTrue(77.94179 == ms_helix_prior.rotate_angles_median(ar, {'do_plot': False, 'output_dir': self.output_dir }))
        clean_up(get_list_of_created_file(cmd=["ls ./*.png"]).split("\n"))

    def test_rotate_angles_median_with_plot_and_with_even_array(self):
        ar = ndarray(shape=(8,), buffer=np_array([79.75458, 55.19391, 77.94179, 80.17834, 78.84809, 71.0277, 77.47843,  77.8888]), dtype=float)
        self.assertTrue(77.94179 == ms_helix_prior.rotate_angles_median(ar, {'do_plot': True,'output_dir': self.output_dir, 'prefix': 'DEFAULT'}))
        clean_up(get_list_of_created_file(cmd=["ls ./*.png"]).split("\n"))



class Test_subtract_and_adjust_angles(unittest.TestCase):

    def test_subtract_and_adjust_angles_array_input(self):
        ar = ndarray(shape=(7,), buffer=np_array([79.75458, 55.19391, 77.94179, 80.17834, 78.84809, 71.0277, 77.47843]), dtype=float)
        self.assertTrue(None == ms_helix_prior.subtract_and_adjust_angles(data_rotated=ar,  value=0,  angle_max=180,  angle_min=-180  ))

    def test_subtract_and_adjust_angles_not_adjust(self):
        self.assertTrue( 111 == ms_helix_prior.subtract_and_adjust_angles(data_rotated=np_int64(111), value=0, angle_max=180, angle_min=-180))

    def test_subtract_and_adjust_angles_smaller_than_min_angle(self):
        self.assertTrue( 368 == ms_helix_prior.subtract_and_adjust_angles(data_rotated=np_int64(8), value=0, angle_max=180, angle_min=10))

    def test_subtract_and_adjust_angles_bigger_than_max_angle(self):
        self.assertTrue(-152 == ms_helix_prior.subtract_and_adjust_angles(data_rotated=np_int64(208), value=0, angle_max=180, angle_min=10))

    def test_subtract_and_adjust_angles_bigger_than_max_angle1(self):
        with self.assertRaises(AssertionError):
            ms_helix_prior.subtract_and_adjust_angles(data_rotated=208, value=0, angle_max=180, angle_min=10)



class Test_rotate_angles_mean(unittest.TestCase):
    def test_rotate_angles_mean(self):
        rotate_angle, nr_outliers = ms_helix_prior.rotate_angles_mean(data_rotated=ndarray(shape=(7,), buffer=np_array([1.81279, -22.74788, 0., 2.23655, 0.9063, -6.91409, -0.46336]), dtype=float), rotate_angle=np_float64(77.94179), tol_mean=30)
        self.assertTrue(0 == nr_outliers and 74.34612 ==rotate_angle )



class Test_identify_outliers_deg(unittest.TestCase):
    def test_identify_outliers_deg_without_outliers(self):
        ar =ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=float)
        expected_inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        expected_outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        is_outlier, inside_tol_idx, outside_tol_idx = ms_helix_prior.identify_outliers_deg(data_rotated=ar, tolerance=15, tolerance_filament=0.2, nr_outliers=0)
        self.assertFalse(is_outlier)
        self.assertTrue(array_equal(expected_inside_tol_idx,inside_tol_idx))
        self.assertTrue((array_equal(expected_outside_tol_idx,outside_tol_idx)))

    def test_identify_outliers_deg_with_outliers(self):
        ar =ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=float)
        expected_inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        expected_outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        is_outlier, inside_tol_idx, outside_tol_idx = ms_helix_prior.identify_outliers_deg(data_rotated=ar, tolerance=15, tolerance_filament=0, nr_outliers=0)
        self.assertTrue(is_outlier)
        self.assertTrue(array_equal(expected_inside_tol_idx,inside_tol_idx))
        self.assertTrue((array_equal(expected_outside_tol_idx,outside_tol_idx)))



class Test_identify_outliers_std(unittest.TestCase):
    def test_identify_outliers_std_Is_outlier(self):
        self.assertTrue(ms_helix_prior.identify_outliers_std(std=8.30777625271, tolerance=15, tolerance_std=2 ))

    def test_identify_outliers_std_Is_Not_outlier(self):
        self.assertFalse(ms_helix_prior.identify_outliers_std(std=8.30777625271, tolerance=15, tolerance_std=1 ))



class Test_get_tolerance_outliers(unittest.TestCase):
    def test_get_tolerance_outliers_1(self):
        inside_tolerance, outside_tolerance = ms_helix_prior.get_tolerance_outliers(ndarray(shape=(7,), buffer=np_array([1.81279, -22.74788, 0., 2.23655, 0.9063, -6.91409, -0.46336]), dtype=float), tolerance=30)
        expected_inside_tolerance = ndarray(shape=(7,), buffer=np_array([1.81279, -22.74788, 0., 2.23655, 0.9063, -6.91409, -0.46336]), dtype=float)
        expected_outside_tolerance = ndarray(shape=(0,),buffer=np_array([]), dtype=float)
        self.assertTrue(array_equal(expected_inside_tolerance, inside_tolerance))
        self.assertTrue(array_equal(expected_outside_tolerance, outside_tolerance))

    def test_get_tolerance_outliers_2(self):
        inside_tolerance, outside_tolerance = ms_helix_prior.get_tolerance_outliers(ndarray(shape=(7,), buffer=np_array([1.81279, -22.74788, 0., 2.23655, 0.9063, -6.91409, -0.46336]), dtype=float), tolerance=3)
        expected_inside_tolerance = ndarray(shape=(5,), buffer=np_array([[ 1.81279 , 0. ,2.23655 , 0.9063 , -0.46336]]), dtype=float)
        expected_outside_tolerance = ndarray(shape=(2,),buffer=np_array([[-22.74788 , -6.91409]]), dtype=float)
        self.assertTrue(array_equal(expected_inside_tolerance, inside_tolerance))
        self.assertTrue(array_equal(expected_outside_tolerance, outside_tolerance))



class Test_find_tolerance_outliers(unittest.TestCase):
    def test_find_tolerance_outliers_where_the_outliers_are_less_than_half_array(self):
        ar =ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=float)
        expected_inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        expected_outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        inside_tol_idx, outside_tol_idx = ms_helix_prior.find_tolerance_outliers(input_array=ar, tolerance=15,  nr_outliers=1)
        self.assertTrue(array_equal(expected_inside_tol_idx,inside_tol_idx))
        self.assertTrue((array_equal(expected_outside_tol_idx,outside_tol_idx)))

    def test_find_tolerance_outliers_where_the_outliers_are_more_than_half_array(self):
        ar =ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=float)
        expected_inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        expected_outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        inside_tol_idx, outside_tol_idx = ms_helix_prior.find_tolerance_outliers(input_array=ar, tolerance=15,  nr_outliers=4)
        self.assertTrue(array_equal(expected_inside_tol_idx,inside_tol_idx))
        self.assertTrue((array_equal(expected_outside_tol_idx,outside_tol_idx)))



class Test_calculate_prior_values_running(unittest.TestCase):
    def test_calculate_prior_values_running(self):
        data_rotated = ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=np_float64)
        prior_array = ndarray(shape=(7,), buffer=np_array([  6.04271832e-154, 4.94840066e+173 ,  0.00000000e+000 ,  0.00000000e+000 ,  9.07685909e+223,   0.00000000e+000  , 0.00000000e+000]), dtype=np_float64)
        window_size = 3
        inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        self.assertTrue(ms_helix_prior.calculate_prior_values_running(data_rotated, prior_array, window_size, inside_tol_idx, outside_tol_idx,))




class Test_calc_chi_square(unittest.TestCase):
    def test_calc_chi_square1(self):
        fit_dim = 1
        x_values = ndarray(shape=(6,), buffer=np_array([0, 2, 3, 4, 5, 6]), dtype=np_int64)
        y_values = ndarray(shape=(6,), buffer=np_array([5.40846, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]),dtype=np_float64)
        params = ndarray(shape=(2,), buffer=np_array([-0.81184543, 5.89818643]), dtype=np_float64)
        self.assertTrue( (abs(10.1931805627 -  ms_helix_prior.calc_chi_square(y_values, x_values, params, fit_dim, func_dict[fit_dim]['func'])) < 0.000000001) )



class Test_calculate_prior_values_fit(unittest.TestCase):
    def test_calculate_prior_values_fit(self):
        data_rotated = ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=np_float64)
        prior_array = ndarray(shape=(7,), buffer=np_array([  6.04271832e-154, 4.94840066e+173 ,  0.00000000e+000 ,  0.00000000e+000 ,  9.07685909e+223,   0.00000000e+000  , 0.00000000e+000]), dtype=np_float64)
        inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        self.assertTrue(None ==ms_helix_prior.calculate_prior_values_fit(data_rotated, prior_array, inside_tol_idx))



class Test_mark_as_outlier(unittest.TestCase):
    inside_tol_idx=np_array([1])
    outside_tol_idx=np_array([0, 2])

    def test_data_is_outlier_and_force(self):
        data = np_array([(999,), (999,), (999,)], dtype=[('a', '<i8')])
        ms_helix_prior.mark_as_outlier(array = data['a'], is_outlier=True, force_outlier=True, inside_tol_idx=self.inside_tol_idx, outside_tol_idx=self.outside_tol_idx)
        aspected_result = ndarray(shape=(3,), buffer=np_array([1, 1, 1]), dtype=int)
        self.assertTrue(array_equal(aspected_result, data['a']))

    def test_data_is_outlier_but_no_force(self):
        data = np_array([(999,), (999,), (999,)], dtype=[('a', '<i8')])
        ms_helix_prior.mark_as_outlier(array = data['a'], is_outlier=True, force_outlier=False, inside_tol_idx=self.inside_tol_idx, outside_tol_idx=self.outside_tol_idx)
        aspected_result = ndarray(shape=(3,), buffer=np_array([1, 1, 1]), dtype=int)
        self.assertTrue(array_equal(aspected_result, data['a']))

    def test_data_is_no_outlier_but_force(self):
        data = np_array([(999,), (999,), (999,)], dtype=[('a', '<i8')])
        ms_helix_prior.mark_as_outlier(array = data['a'], is_outlier=False, force_outlier=True, inside_tol_idx=self.inside_tol_idx, outside_tol_idx=self.outside_tol_idx)
        aspected_result = ndarray(shape=(3,), buffer=np_array([0, 0, 0]), dtype=int)
        self.assertTrue(array_equal(aspected_result, data['a']))

    def test_data_is_no_outlier_and__no_force(self):
        data = np_array([(999,), (999,), (999,)], dtype=[('a', '<i8')])
        ms_helix_prior.mark_as_outlier(array = data['a'], is_outlier=False, force_outlier=False, inside_tol_idx=self.inside_tol_idx, outside_tol_idx=self.outside_tol_idx)
        aspected_result = ndarray(shape=(3,), buffer=np_array([1, 0, 1]), dtype=int)
        self.assertTrue(array_equal(aspected_result, data['a']))



class Test_calculate_prior_values_linear(unittest.TestCase):
    def test_calculate_prior_values_linear(self):
        data_rotated = ndarray(shape=(7,), buffer=np_array([5.40846, -19.15221, 3.59567, 5.83222, 4.50197, -3.31842, 3.13231]), dtype=np_float64)
        prior_array = ndarray(shape=(7,), buffer=np_array([  6.04271832e-154, 4.94840066e+173 ,  0.00000000e+000 ,  0.00000000e+000 ,  9.07685909e+223,   0.00000000e+000  , 0.00000000e+000]), dtype=np_float64)
        window_size = 3
        inside_tol_idx = ndarray(shape=(6,), buffer=np_array([0,2,3,4,5,6]), dtype=np_int64)
        outside_tol_idx = ndarray(shape=(1,), buffer=np_array([1]), dtype=np_int64)
        self.assertTrue(ms_helix_prior.calculate_prior_values_linear(data_rotated, prior_array, window_size, inside_tol_idx, outside_tol_idx,))


