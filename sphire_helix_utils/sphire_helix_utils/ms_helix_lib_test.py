import sparx as sp
import ms_helix_lib         # it generates the "close failed in file object destructor: IOError: [Errno 9] Bad file descriptor" error but the tests are working
import unittest
from numpy import array as np_array
from numpy import ndarray,array_equal
from shutil import copy2
from os import remove,rmdir,path

def clean_up(stuff_to_remove):
    for f in stuff_to_remove:
        remove(f)

class Test_identify_outliers(unittest.TestCase):
    data_dtype = [('outlier_angle1', '<i8'), ('outlier_angle2', '<i8'), ('outlier', '<i8')]

    def generate_prior_tracker(self, data_array):
        return {'idx_angle': 0, 'array': np_array(data_array, dtype=self.data_dtype), 'angle_names': [['angle1'], ['angle2']]}

    def test_No_outliers(self):
        pt = self.generate_prior_tracker([(0, 0, 0), (0, 0, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result =ndarray(shape=(2,), buffer=np_array([0,0]),  dtype=int)
        self.assertTrue( array_equal(aspected_result,pt['array']['outlier']) )

    def test_Filament1_and_Filament2outliers_OR_Angle1_and_Angle2_outliers(self):
        pt = self.generate_prior_tracker([(1, 1, 0), (1, 1, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result =ndarray(shape=(2,), buffer=np_array([1,1]),  dtype=int)
        self.assertTrue( array_equal(aspected_result,pt['array']['outlier']) )

    def test_Filament2outlier_OR_Angle1_and_Angle2_outliers(self):
        pt = self.generate_prior_tracker([(0, 0, 0), (1, 1, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result =ndarray(shape=(2,), buffer=np_array([0,1]),  dtype=int)
        self.assertTrue( array_equal(aspected_result,pt['array']['outlier']) )

    def test_Filament1outlier_OR_Angle1_and_Angle2_outliers(self):
        pt = self.generate_prior_tracker([(1, 1, 0), (0, 0, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result =ndarray(shape=(2,), buffer=np_array([1,0]),  dtype=int)
        self.assertTrue( array_equal(aspected_result,pt['array']['outlier']) )

    def test_Filament2outlier_OR_Angle1_outlier(self):
        pt = self.generate_prior_tracker([(0, 0, 0), (1, 0, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result =ndarray(shape=(2,), buffer=np_array([0,1]),  dtype=int)
        self.assertTrue( array_equal(aspected_result,pt['array']['outlier']) )

    def test_Filament2outlier_OR_Angle2_outlier(self):
        pt = self.generate_prior_tracker([(0, 0, 0), (0, 1, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result = ndarray(shape=(2,), buffer=np_array([0, 1]), dtype=int)
        self.assertTrue(array_equal(aspected_result, pt['array']['outlier']))

    def test_Filament1outlier_OR_Angle1_outlier(self):
        pt = self.generate_prior_tracker([(1, 0, 0), (0, 0, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result = ndarray(shape=(2,), buffer=np_array([1, 0]), dtype=int)
        self.assertTrue(array_equal(aspected_result, pt['array']['outlier']))

    def test_Filament1outlier_OR_Angle2_outlier(self):
        pt = self.generate_prior_tracker([(0, 1, 0), (0, 0, 0)])
        ms_helix_lib.identify_outliers(pt)
        aspected_result = ndarray(shape=(2,), buffer=np_array([1, 0]), dtype=int)
        self.assertTrue(array_equal(aspected_result, pt['array']['outlier']))



class Test_combine_and_order_filaments(unittest.TestCase):
    data_dtype = [('col1', '<i8'), ('col2', '<i8')]
    data = np_array([(0, 0), (0, 0), (0, 0), (0, 0)], dtype = data_dtype)
    data_filament = np_array([np_array([(1, 4), (2, 3)], dtype = data_dtype), np_array([(3, 2), (4, 1)], dtype = data_dtype)])

    def generate_prior_tracker(self, order):
        return {'array': self.data, 'array_filament': self.data_filament, 'order': order}

    def test_col1_greater_col2(self):
        pt = self.generate_prior_tracker(['col1', 'col2'])
        ms_helix_lib.combine_and_order_filaments(pt)
        aspected_result0 = np_array([(1, 4)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result1 = np_array([(2, 3)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result2 = np_array([(3, 2)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result3 = np_array([(4,1)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]

        self.assertTrue(array_equal(aspected_result0,  pt['array'][0]) and array_equal(aspected_result1,  pt['array'][1])
                        and array_equal(aspected_result2,  pt['array'][2]) and array_equal(aspected_result3,  pt['array'][3])  )

    def test_col2_greater_col1(self):
        pt = self.generate_prior_tracker(['col2', 'col1'])
        ms_helix_lib.combine_and_order_filaments(pt)
        aspected_result3 = np_array([(1, 4)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result2 = np_array([(2, 3)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result1 = np_array([(3, 2)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]
        aspected_result0 = np_array([(4,1)], dtype=[('col1', '<i8'), ('col2', '<i8')])[0]

        self.assertTrue(array_equal(aspected_result0,  pt['array'][0]) and array_equal(aspected_result1,  pt['array'][1])
                        and array_equal(aspected_result2,  pt['array'][2]) and array_equal(aspected_result3,  pt['array'][3])  )

    def test_raiseException_unknown_field_name(self):
        pt1=self.generate_prior_tracker(['col1', 'col1'])
        pt2 = self.generate_prior_tracker(['col2', 'col2'])
        with self.assertRaises(ValueError):
            ms_helix_lib.combine_and_order_filaments(pt1)
            ms_helix_lib.combine_and_order_filaments(pt2)



class Test_import_data_sphire(unittest.TestCase):
    params_file_raw = '../tests/index_raw.txt'
    index_file_raw = '../tests/params_raw.txt'
    params_file = 'index.txt'
    index_file = 'params.txt'


    def create_prior_tracker(self,tracker):
        copy2(self.index_file_raw, self.params_file)
        copy2(self.params_file_raw, self.index_file)
        return  ms_helix_lib.import_data_sphire(tracker, False, self.params_file, self.index_file)

    def test_tracker_is_filename(self):
        prior_tracker = self.create_prior_tracker(tracker = 'bdb:../tests/stack')

        self.assertTrue(16 == len(prior_tracker))
        self.assertTrue(684 == len(prior_tracker['array']))
        aspected_output =['angle_min', 'micrograph_id', 'segment_id', 'output_dir', 'output_file_params', 'idx_angle_prior', 'output_file_index', 'tracker', 'filament_id', 'angle_names', 'idx_angle', 'array', 'angle_max', 'order', 'idx_angle_rot', 'output_columns']
        self.assertTrue(aspected_output == prior_tracker.keys())
        aspected_output = ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 0,  38.32375,  79.75458,  278.43793,  8.00109,  1.00109,  0.19693,  0.73653,  91259.15828, 0, 0)
        self.assertTrue(aspected_output, prior_tracker['array'][0])
        aspected_output = ('filt_Factin_ADP_cLys_0009_falcon2.hdf', 'filt_Factin_ADP_cLys_0009_falcon2.hdf0009', 7,  38.40719,  82.93683,  298.12543, -7.48667,  15.25721,  0.5188,  0.73356,  90890.99319, 683, 683)
        self.assertTrue(aspected_output, prior_tracker['array'][-1])
        aspected_output = ('ptcl_source_image', 'filament', 'data_n', 'phi', 'theta', 'psi', 'shift_x', 'shift_y', 'err1', 'err2', 'norm', 'source_n', 'stack_idx')
        self.assertTrue(aspected_output == prior_tracker['array'].dtype.names)
        clean_up([self.params_file, self.index_file])

    def test_tracker_is_dictionary_and_contains_array(self):
        prior_tracker = self.create_prior_tracker(tracker = 'bdb:../tests/stack')
        tracker = {'constants': {'stack_prior': prior_tracker['array'][['ptcl_source_image', 'filament', 'data_n']]}}
        prior_tracker = self.create_prior_tracker(tracker=tracker)

        self.assertTrue(16 == len(prior_tracker))
        self.assertTrue(684 == len(prior_tracker['array']))
        aspected_output =['angle_min', 'micrograph_id', 'segment_id', 'output_dir', 'output_file_params', 'idx_angle_prior', 'output_file_index', 'tracker', 'filament_id', 'angle_names', 'idx_angle', 'array', 'angle_max', 'order', 'idx_angle_rot', 'output_columns']
        self.assertTrue(aspected_output == prior_tracker.keys())
        aspected_output = ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 0,  38.32375,  79.75458,  278.43793,  8.00109,  1.00109,  0.19693,  0.73653,  91259.15828, 0, 0)
        self.assertTrue(aspected_output, prior_tracker['array'][0])
        aspected_output = ('filt_Factin_ADP_cLys_0009_falcon2.hdf', 'filt_Factin_ADP_cLys_0009_falcon2.hdf0009', 7,  38.40719,  82.93683,  298.12543, -7.48667,  15.25721,  0.5188,  0.73356,  90890.99319, 683, 683)
        self.assertTrue(aspected_output, prior_tracker['array'][-1])
        aspected_output = ('ptcl_source_image', 'filament', 'data_n', 'phi', 'theta', 'psi', 'shift_x', 'shift_y', 'err1', 'err2', 'norm', 'source_n', 'stack_idx')
        self.assertTrue(aspected_output == prior_tracker['array'].dtype.names)
        clean_up([self.params_file, self.index_file])


    def test_tracker_is_dictionary_and_contains_filename(self):
        tracker = {'constants': {'stack': 'bdb:../tests/stack'}}
        prior_tracker = self.create_prior_tracker(tracker=tracker)
        self.assertTrue(16 == len(prior_tracker))
        self.assertTrue(684 == len(prior_tracker['array']))
        aspected_output = ['angle_min', 'micrograph_id', 'segment_id', 'output_dir', 'output_file_params','idx_angle_prior', 'output_file_index', 'tracker', 'filament_id', 'angle_names', 'idx_angle', 'array', 'angle_max', 'order', 'idx_angle_rot', 'output_columns']
        self.assertTrue(aspected_output == prior_tracker.keys())
        aspected_output = ('filt_Factin_ADP_cLys_0005_falcon2.hdf', 'filt_Factin_ADP_cLys_0005_falcon2.hdf0000', 0, 38.32375, 79.75458, 278.43793, 8.00109, 1.00109, 0.19693, 0.73653, 91259.15828, 0, 0)
        self.assertTrue(aspected_output, prior_tracker['array'][0])
        aspected_output = ('filt_Factin_ADP_cLys_0009_falcon2.hdf', 'filt_Factin_ADP_cLys_0009_falcon2.hdf0009', 7, 38.40719, 82.93683,  298.12543, -7.48667, 15.25721, 0.5188, 0.73356, 90890.99319, 683, 683)
        self.assertTrue(aspected_output, prior_tracker['array'][-1])
        aspected_output = ('ptcl_source_image', 'filament', 'data_n', 'phi', 'theta', 'psi', 'shift_x', 'shift_y', 'err1', 'err2', 'norm', 'source_n', 'stack_idx')
        self.assertTrue(aspected_output == prior_tracker['array'].dtype.names)
        clean_up([self.params_file, self.index_file])



class Test_import_data_relion(unittest.TestCase):
    def test_import_a_relion_star_file(self):
        prior_tracker = ms_helix_lib.import_data_relion(file_name = '../tests/data_test.star')
        self.assertTrue(14 == len(prior_tracker))
        self.assertTrue(274 == len(prior_tracker['array']))
        aspected_output = ['angle_min', 'micrograph_id', 'segment_id', 'output_dir', 'output_file', 'idx_angle_prior', 'filament_id', 'angle_names', 'idx_angle', 'array', 'angle_max', 'order', 'idx_angle_rot', 'output_columns']
        self.assertTrue(aspected_output == prior_tracker.keys())
        aspected_output = (677.583313, 857.861694, 1, 0.0, '000001@Extract/job059/corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrcs', 'corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrc', 300.0, 20550.580078, 20305.132812, 23.187677, 0.0, 0.0, 1.0, 0.0, 0.1, 122807.0, 18.666667, 999.0, 0.006135, 1, -108.651069, 80.049875, -64.364309, -6.373347, 1.626653, 1, 0.808728, 1, 135071.7, 0.113652, 8, 0)
        self.assertTrue(aspected_output, prior_tracker['array'][0])
        aspected_output = (2896.461182, 1781.382568, 20, 592.000054, '000274@Extract/job059/corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrcs', 'corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrc', 300.0, 20550.580078, 20305.132812, 23.187677, 0.0, 0.0, 1.0, 0.0, 0.1, 122807.0, 18.666667, 999.0, 0.006135, 1, 149.725232, 87.340771, -138.469118, -4.901477, 2.098523, 1, 0.806169, 1, 134355.0, 0.172743, 20, 273)
        self.assertTrue(aspected_output, prior_tracker['array'][-1])
        aspected_output = ('_rlnCoordinateX', '_rlnCoordinateY', '_rlnHelicalTubeID', '_rlnHelicalTrackLength', '_rlnImageName', '_rlnMicrographName', '_rlnVoltage', '_rlnDefocusU', '_rlnDefocusV', '_rlnDefocusAngle', '_rlnSphericalAberration', '_rlnCtfBfactor', '_rlnCtfScalefactor', '_rlnPhaseShift', '_rlnAmplitudeContrast', '_rlnMagnification', '_rlnDetectorPixelSize', '_rlnCtfMaxResolution', '_rlnCtfFigureOfMerit', '_rlnGroupNumber', '_rlnAngleRot', '_rlnAngleTilt', '_rlnAnglePsi', '_rlnOriginX', '_rlnOriginY', '_rlnClassNumber', '_rlnNormCorrection', '_rlnRandomSubset', '_rlnLogLikeliContribution', '_rlnMaxValueProbDistribution', '_rlnNrOfSignificantSamples', 'source_n')
        self.assertTrue(aspected_output == prior_tracker['array'].dtype.names)



class Test_expand_and_order_array(unittest.TestCase):
    def test_expand_and_order_array(self):
        data = np_array([(0, 1, 2, 3, 4), (0, 1, 2, 3, 4), (0, 1, 2, 3, 4), (0, 1, 2, 3, 4)],
                        dtype=[('col1', '<i8'), ('col2', '<i8'), ('col3', '<i8'), ('angle1', '<i8'), ('angle2', '<i8')])
        prior_tracker = {}
        prior_tracker['angle_names'] = [['angle1', 'angle1_prior', 'angle1_rot'], ['angle2', 'angle2_prior', 'angle2_rot']]
        prior_tracker['array'] = data
        prior_tracker['idx_angle'] = 0
        prior_tracker['idx_angle_prior'] = 1
        prior_tracker['idx_angle_rot'] = 2
        prior_tracker['micrograph_id'] = 'col1'
        prior_tracker['filament_id'] = 'col2'
        prior_tracker['segment_id'] = 'col3'
        prior_tracker['output_columns'] = ['col1', 'col2', 'col3']
        prior_tracker = ms_helix_lib.expand_and_order_array(prior_tracker=prior_tracker)
        self.assertTrue(5 == len(prior_tracker['output_columns']))
        self.assertTrue(4 == len(prior_tracker['array']))
        self.assertTrue(12 == len(prior_tracker['array'][0]))



class Test_loop_filaments(unittest.TestCase):
    @staticmethod
    def generate_prior_tracker(apply_method = "invalid"):
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

    def test_loop_filaments_with_DEG_apply_method(self):
        prior_tracker = ms_helix_lib.loop_filaments(prior_tracker= self.generate_prior_tracker("deg"))
        self.assertTrue(isinstance(prior_tracker, dict))
        rmdir('prior_images_0')

    def test_loop_filaments_with_STD_apply_method(self):
        prior_tracker = ms_helix_lib.loop_filaments(prior_tracker= self.generate_prior_tracker("std"))
        self.assertTrue(isinstance(prior_tracker, dict))
        rmdir('prior_images_0')

    def test_loop_filaments_with_NOT_SPECIFIED_apply_method(self):
        prior_tracker = ms_helix_lib.loop_filaments(prior_tracker= self.generate_prior_tracker())
        self.assertTrue(isinstance(prior_tracker, dict))
        rmdir('prior_images_0')



class Test_export_data_relion(unittest.TestCase):
    dtype = [('col1', '<i8'), ('col2', '<i8'), ('col3', '<i8'), ('angle1', '<i8'), ('outlier', '<i8')]
    output_columns = ['col1', 'col2', 'col3']
    output_file_name = 'doctest'
    output_file = 'doctest_prior.star'

    def generate_prior_tracker(self, data, do_discard_outlier):
        return {'array': data, 'output_columns': self.output_columns, 'output_file': self.output_file_name, 'outlier': 'outlier', 'do_discard_outlier': do_discard_outlier}

    def test_export_without_outliers_OR_remove_outlier_from_file(self):
        data = np_array([(0, 1, 2, 3, 0), (5, 6, 7, 8, 0), (10, 11, 12, 13, 0), (15, 16, 17, 18, 0)], dtype = self.dtype)
        prior_tracker = self.generate_prior_tracker(data, True)
        ms_helix_lib.export_data_relion(prior_tracker=prior_tracker)
        self.assertTrue(path.exists(self.output_file))
        with open(self.output_file, 'r') as read:
            lines = read.readlines()
        self.assertTrue(11 == len(lines))
        self.assertTrue(len(self.output_columns) == len(lines[-1].split()))
        clean_up([self.output_file])

    def test_with_one_outlier_in_the_beginning_OR_Remove_outlier_from_file(self):
        data = np_array([(0, 1, 2, 3, 1), (5, 6, 7, 8, 0), (10, 11, 12, 13, 0), (15, 16, 17, 18, 0)], dtype = self.dtype)
        prior_tracker = self.generate_prior_tracker(data, True)
        ms_helix_lib.export_data_relion(prior_tracker=prior_tracker)
        self.assertTrue(path.exists(self.output_file))
        with open(self.output_file, 'r') as read:
            lines = read.readlines()
        self.assertTrue(10 == len(lines))
        self.assertTrue(len(self.output_columns) == len(lines[-1].split()))
        clean_up([self.output_file])

    def test_with_one_outlier_in_the_beginning_AND_one_in_the_end_OR_remove_outlier_from_file(self):
        data = np_array([(0, 1, 2, 3, 1), (5, 6, 7, 8, 0), (10, 11, 12, 13, 0), (15, 16, 17, 18, 1)], dtype = self.dtype)
        prior_tracker = self.generate_prior_tracker(data, True)
        ms_helix_lib.export_data_relion(prior_tracker=prior_tracker)
        self.assertTrue(path.exists(self.output_file))
        with open(self.output_file, 'r') as read:
            lines = read.readlines()
        self.assertTrue(9 == len(lines))
        self.assertTrue(len(self.output_columns) == len(lines[-1].split()))
        clean_up([self.output_file])

    def test_with_one_outlier_in_the_beginning_AND_one_in_the_end_OR_dont_remove_outlier_from_file(self):
        data = np_array([(0, 1, 2, 3, 1), (5, 6, 7, 8, 0), (10, 11, 12, 13, 0), (15, 16, 17, 18, 1)], dtype = self.dtype)
        prior_tracker = self.generate_prior_tracker(data, False)
        ms_helix_lib.export_data_relion(prior_tracker=prior_tracker)
        self.assertTrue(path.exists(self.output_file))
        with open(self.output_file, 'r') as read:
            lines = read.readlines()
        self.assertTrue(11 == len(lines))
        self.assertTrue(len(self.output_columns) == len(lines[-1].split()))
        clean_up([self.output_file])



class Test_export_data_sphire(unittest.TestCase):
    params_file_raw = '../tests/params_raw.txt'
    index_file_raw = '../tests/index_raw.txt'
    params_file = 'params.txt'
    index_file = 'index.txt'
    data = np_array([(0, 1, 2, 3, 0, 1, 2, 0, 0), (5, 6, 7, 8, 0, 1, 2, 0, 1), (10, 11, 12, 13, 0, 1, 2, 0, 2), (15, 16, 17, 18, 0, 1, 2, 1, 3)], dtype = [('angle1_prior', '<i8'), ('phi', '<i8'), ('shift_x', '<i8'), ('shift_y', '<i8'), ('err1', '<i8'),('err2', '<i8'), ('norm', '<i8'), ('outlier', '<i8'), ('stack_idx', '<i8')])
    output_columns = ['col1', 'col2', 'col3']
    output_file_params = 'params'
    output_file_index = 'index'


    def generate_prior_tracker(self,apply_prior, do_discard_outlier, state):
        copy2(self.index_file_raw, 'index.txt')
        copy2(self.params_file_raw, 'params.txt')
        return {'array': self.data, 'output_columns': self.output_columns,'output_file_params': self.output_file_params,'output_file_index': self.output_file_index, 'idx_angle_prior':1, 'angle_names': [['angle1', 'angle1_prior', 'angle1_rot']], 'outlier': 'outlier', 'tracker': {'constants': {'apply_prior': apply_prior}, 'state': state}, 'do_discard_outlier': do_discard_outlier}

    def test_one_outlier_OR_tracker_dict_RESTRICTED_OR_Dont_discard_outliers(self):
        prior_tracker = self.generate_prior_tracker(apply_prior=True, do_discard_outlier=False, state='RESTRICTED')
        ms_helix_lib.export_data_sphire(prior_tracker=prior_tracker)

        with open('{0}.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(4 == len(lines))
        self.assertTrue(7 == len(lines[-1].split()))
        self.assertTrue('     16     15     17     18      0      1      2\n' == lines[-1])

        with open('{0}_prior.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(8 == len(lines[-1].split()))
        self.assertTrue('      38.40719      82.93683     298.12543      -7.48667      15.25721       0.51880       0.73356   90890.99319\n' == lines[-1])


        with open('{0}.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(4 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('      3\n' ==  lines[-1])

        with open('{0}_prior.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('683\n' == lines[-1])

        clean_up(['index.txt', 'index_prior.txt','params.txt', 'params_prior.txt'])

    def test_one_outlier_OR_tracker_dict_outlier_RESTRICTED_OR_discard_outliers(self):
        prior_tracker = self.generate_prior_tracker(apply_prior=True, do_discard_outlier=True, state='RESTRICTED')
        ms_helix_lib.export_data_sphire(prior_tracker=prior_tracker)

        with open('{0}.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(3 == len(lines))
        self.assertTrue(7 == len(lines[-1].split()))
        self.assertTrue('     11     10     12     13      0      1      2\n' == lines[-1])

        with open('{0}_prior.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(8 == len(lines[-1].split()))
        self.assertTrue('      38.40719      82.93683     298.12543      -7.48667      15.25721       0.51880       0.73356   90890.99319\n' == lines[-1])


        with open('{0}.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(3 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('      2\n' ==  lines[-1])

        with open('{0}_prior.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('683\n' == lines[-1])

        clean_up(['index.txt', 'index_prior.txt','params.txt', 'params_prior.txt'])

    def test_one_outlier_OR_tracker_dict_outlier_EXHAUSTIVE_OR_discard_outliers(self):
        prior_tracker = self.generate_prior_tracker(apply_prior=True, do_discard_outlier=True, state='EXHAUSTIVE')
        ms_helix_lib.export_data_sphire(prior_tracker=prior_tracker)

        with open('{0}.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(8 == len(lines[-1].split()))
        self.assertTrue('      38.40719      82.93683     298.12543      -7.48667      15.25721       0.51880       0.73356   90890.99319\n' == lines[-1])

        with open('{0}_prior.txt_not_applied.txt'.format(self.output_file_params), 'r') as read:
            lines = read.readlines()
        self.assertTrue(3 == len(lines))
        self.assertTrue(7 == len(lines[-1].split()))
        self.assertTrue('     11     10     12     13      0      1      2\n' == lines[-1])

        with open('{0}.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('683\n' ==  lines[-1])

        with open('{0}_prior.txt_not_applied.txt'.format(self.output_file_index), 'r') as read:
            lines = read.readlines()
        self.assertTrue(3 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('      2\n' == lines[-1])

        clean_up(['index.txt', 'index_prior.txt_not_applied.txt','params.txt', 'params_prior.txt_not_applied.txt'])


class Test_plot_polar(unittest.TestCase):
    def test_if_plt(self):
        ms_helix_lib.plot_polar(name='doctest', array=np_array([0, 1, 2, 3]), angle_rotation=3, angle_max=360, angle_min=0)
        ms_helix_lib.plot_polar(name='doctest', array=np_array([0, 1, 2, 3]), angle_rotation=3, angle_max=180, angle_min=-180)
        ms_helix_lib.plot_polar(name='doctest', array=np_array([0, 1, 2, 3]), angle_rotation=3, angle_max=90, angle_min=0)
        ms_helix_lib.plot_polar(name='doctest', array=np_array([0, 1, 2, 3]), angle_rotation=3, angle_max=360, angle_min=0, mean=20, tol=5, old_mean=8)
        self.assertTrue(path.exists('DEFAULT_0_doctest.png'))
        self.assertTrue(path.exists('DEFAULT_1_doctest.png'))
        self.assertTrue(path.exists('DEFAULT_2_doctest.png'))
        self.assertTrue(path.exists('DEFAULT_3_doctest.png'))
        clean_up(['DEFAULT_0_doctest.png','DEFAULT_1_doctest.png','DEFAULT_2_doctest.png','DEFAULT_3_doctest.png'])