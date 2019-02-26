import ms_helix_lib         # it generates the "close failed in file object destructor: IOError: [Errno 9] Bad file descriptor" error but the tests are working
import unittest
from numpy import array as np_array
from numpy import ndarray,array_equal, empty


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


