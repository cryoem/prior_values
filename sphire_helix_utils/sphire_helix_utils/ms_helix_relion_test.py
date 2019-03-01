import ms_helix_relion
import unittest
from numpy import array as np_array
from numpy import array_equal
from os import remove,path

def clean_up(stuff_to_remove):
    for f in stuff_to_remove:
        if path.exists(f) and path.isfile(f):
            remove(f)

class Test_ms_helix_relion(unittest.TestCase):
    file_name = '../tests/data_test.star'
    output_file_name = 'doctest'
    output_file = 'doctest_prior.star'

    def test_create_dtype_dict(self):
        dtype_list = {'_rlnNrOfSignificantSamples': '<i8', '_rlnClassNumber': '<i8', '_rlnGroupNumber': '<i8', '_rlnDetectorPixelSize': '<f8', '_rlnParticleSelectZScore': '<f8', '_rlnHelicalTrackLength': '<f8', '_rlnImageName': '|S200', '_rlnHelicalTubeID': '<i8', '_rlnOriginYPrior': '<f8', '_rlnDefocusU': '<f8', '_rlnDefocusV': '<f8', '_rlnAutopickFigureOfMerit': '<f8', '_rlnMagnification': '<f8', '_rlnNrOfFrames': '<i8', '_rlnOriginalParticleName': '|S200', '_rlnAngleRot': '<f8', '_rlnRandomSubset': '<i8', '_rlnGroupName': '|S200', '_rlnOriginX': '<f8', '_rlnOriginY': '<f8', '_rlnAnglePsiPrior': '<f8', '_rlnLogLikeliContribution': '<f8', '_rlnMicrographName': '|S200', '_rlnNormCorrection': '<f8', '_rlnAngleRotPrior': '<f8', '_rlnCoordinateX': '<f8', '_rlnCoordinateY': '<f8', '_rlnAngleTilt': '<f8', '_rlnOriginXPrior': '<f8', '_rlnSphericalAberration': '<f8', '_rlnAmplitudeContrast': '<f8', '_rlnVoltage': '<f8', '_rlnCtfImage': '|S200', '_rlnAngleTiltPrior': '<f8', '_rlnCtfFigureOfMerit': '<f8', '_rlnMaxValueProbDistribution': '<f8', '_rlnDefocusAngle': '<f8', '_rlnAnglePsi': '<f8'}
        self.assertTrue(dtype_list == ms_helix_relion.create_dtype_dict())

    def test_import_star_file(self):
        expected_header_as_list=['_rlnCoordinateX', '_rlnCoordinateY', '_rlnHelicalTubeID', '_rlnHelicalTrackLength', '_rlnImageName', '_rlnMicrographName', '_rlnVoltage', '_rlnDefocusU', '_rlnDefocusV', '_rlnDefocusAngle', '_rlnSphericalAberration', '_rlnCtfBfactor', '_rlnCtfScalefactor', '_rlnPhaseShift', '_rlnAmplitudeContrast', '_rlnMagnification', '_rlnDetectorPixelSize', '_rlnCtfMaxResolution', '_rlnCtfFigureOfMerit', '_rlnGroupNumber', '_rlnAngleRot', '_rlnAngleTilt', '_rlnAnglePsi', '_rlnOriginX', '_rlnOriginY', '_rlnClassNumber', '_rlnNormCorrection', '_rlnRandomSubset', '_rlnLogLikeliContribution', '_rlnMaxValueProbDistribution', '_rlnNrOfSignificantSamples']
        ar, header, path = ms_helix_relion.import_star_file(input_star_file=self.file_name)
        aspected_output = (2896.461182, 1781.382568, 20, 592.000054, '000274@Extract/job059/corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrcs', 'corrfull_1_39/Factin_ADP_cLys_0005_falcon2_DW.mrc', 300.0, 20550.580078, 20305.132812, 23.187677, 0.0, 0.0, 1.0, 0.0, 0.1, 122807.0, 18.666667, 999.0, 0.006135, 1, 149.725232, 87.340771, -138.469118, -4.901477, 2.098523, 1, 0.806169, 1, 134355.0, 0.172743, 20, 273)
        self.assertTrue(aspected_output, ar[-1])
        self.assertTrue(array_equal(np_array(expected_header_as_list), header))
        self.assertTrue(array_equal(np_array(self.file_name), path))

    def test_create_header_string(self):
        pt ={'output_columns': ['col1', 'col2', 'col3']}
        self.assertTrue("\ndata_\n\nloop\ncol1 #\ncol2 #2\ncol3 #3\n", ms_helix_relion.create_header_string(pt['output_columns']))

    def test_write_star_file(self):
        data = np_array([(0, 1, 2, 3, 0), (5, 6, 7, 8, 0), (10, 11, 12, 13, 0), (15, 16, 17, 18, 0)], dtype= [('col1', '<i8'), ('col2', '<i8'), ('col3', '<i8'), ('angle1', '<i8'), ('outlier', '<i8')])
        output_columns = ['col1', 'col2', 'col3']
        prior_tracker = {'array': data, 'output_columns': output_columns, 'output_file': self.output_file_name, 'outlier': 'outlier', 'do_discard_outlier': True}

        ms_helix_relion.write_star_file(output_array=prior_tracker['array'][prior_tracker['output_columns']], header_string=ms_helix_relion.create_header_string(prior_tracker['output_columns']), output_file='{0}_prior.star'.format(prior_tracker['output_file']), outliers=prior_tracker['array'][prior_tracker['outlier']], do_discard_outlier=prior_tracker['do_discard_outlier'])
        self.assertTrue(path.exists(self.output_file))
        with open(self.output_file, 'r') as read:
            lines = read.readlines()
        self.assertTrue(11 == len(lines))
        self.assertTrue(len(output_columns) == len(lines[-1].split()))
        clean_up([self.output_file])


