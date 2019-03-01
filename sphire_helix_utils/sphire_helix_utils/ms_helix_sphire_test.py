import ms_helix_sphire
import unittest
from os import system as os_system
from os import remove, path
from numpy import array as np_array
from shutil import copy2

RELATIVE_PATH_EMAN2= "../../EMAN2DB"
NAME = 'bdb:stack'
INDEX_FILE_RAW = '../tests/index_raw.txt'
PARAMS_FILE_RAW = '../tests/params_raw.txt'
NEW_INDEX_FILE_RAW = 'new_index.txt'
NEW_PARAMS_FILE_RAW = 'new_params.txt'


def clean_up(stuff_to_remove):
    for f in stuff_to_remove:
        if path.exists(f) and path.isfile(f):
            remove(f)

class Test_ms_helix_sphire(unittest.TestCase):
    SKIP_TEST = False
    pt_data = np_array([(0, 1, 2, 3, 0, 1, 2, 0, 0), (5, 6, 7, 8, 0, 1, 2, 0, 1), (10, 11, 12, 13, 0, 1, 2, 0, 2),(15, 16, 17, 18, 0, 1, 2, 1, 3)], dtype=[('angle1_prior', '<i8'), ('phi', '<i8'), ('shift_x', '<i8'), ('shift_y', '<i8'), ('err1', '<i8'), ('err2', '<i8'), ('norm', '<i8'), ('outlier', '<i8'), ('stack_idx', '<i8')])
    output_file_params = 'params.txt'
    output_file_index = 'index.txt'

    def generate_prior_tracker(self):
        copy2(INDEX_FILE_RAW, self.output_file_index)
        copy2(PARAMS_FILE_RAW, self.output_file_params)
        return {'array': self.pt_data, 'idx_angle_prior': 1, 'angle_names': [['angle1', 'angle1_prior', 'angle1_rot']], 'outlier': 'outlier', 'tracker': {'constants': {'apply_prior': True}, 'state': 'RESTRICTED'}, 'do_discard_outlier': False}

    @classmethod
    def setUpClass(cls):
        print "\n\tcopying EMAN2DB folder"
        os_system("cp ../../EMAN2DB/ -r .")
        try:
            cls.dataDB=ms_helix_sphire.import_sphire_stack(NAME)
        except RuntimeError:
            cls.SKIP_TEST = True
            print ("\n\tWARNING: CANNOT IMPORT THE DB\n\tWARNING: CANNOT IMPORT THE DB\n\tWARNING: CANNOT IMPORT THE DB")

    def test_get_stack_dtype(self):
        dtype_list = [('ptcl_source_image', '|S200'),('filament', '|S200'),('data_n', '<i8')]
        self.assertTrue(dtype_list == ms_helix_sphire.get_stack_dtype())

    def test_import_sphire_stack(self):
        if self.SKIP_TEST is False:
            self.assertTrue(684 == len(self.dataDB))
            self.assertTrue(self.dataDB.dtype == [('ptcl_source_image', 'S200'), ('filament', 'S200'), ('data_n', '<i8')])

    def test_import_sphire_params(self):
        data = ms_helix_sphire.import_sphire_params(PARAMS_FILE_RAW)
        self.assertTrue(data.dtype == [('phi', '<f8'), ('theta', '<f8'), ('psi', '<f8'), ('shift_x', '<f8'), ('shift_y', '<f8'), ('err1', '<f8'),('err2', '<f8'), ('norm', '<f8'), ('source_n', '<i8')])
        self.assertTrue(684 == len(data))

    def test_import_sphire_index(self):
        data = ms_helix_sphire.import_sphire_index(INDEX_FILE_RAW)
        self.assertTrue(data.dtype == [('stack_idx', '<i8')])
        self.assertTrue(684 == len(data))

    def test_write_params_file(self):
        pt = self.generate_prior_tracker()
        ms_helix_sphire.write_index_file(array=pt['array'], file_name=NEW_PARAMS_FILE_RAW, file_name_old=self.output_file_params, prior_tracker=pt)

        self.assertTrue(path.exists(NEW_PARAMS_FILE_RAW) and path.isfile(NEW_PARAMS_FILE_RAW))
        with open(NEW_PARAMS_FILE_RAW, 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(8 == len(lines[-1].split()))
        self.assertTrue('      38.40719      82.93683     298.12543      -7.48667      15.25721       0.51880       0.73356   90890.99319\n' == lines[-1])
        clean_up(["new_params.txt", "params.txt", "index.txt"])

    def test_write_index_file(self):
        pt = self.generate_prior_tracker()
        ms_helix_sphire.write_index_file(array=pt['array'], file_name=NEW_INDEX_FILE_RAW, file_name_old=self.output_file_index, prior_tracker=pt)

        self.assertTrue(path.exists(NEW_INDEX_FILE_RAW) and path.isfile(NEW_INDEX_FILE_RAW))
        with open(NEW_INDEX_FILE_RAW, 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('683\n' == lines[-1])
        clean_up(["new_index.txt"])

    def test_write_file(self):
        pt = self.generate_prior_tracker()
        output_name = ms_helix_sphire.prepare_output(tracker=pt['tracker'],file_name=NEW_INDEX_FILE_RAW,file_name_old=self.output_file_index)
        ms_helix_sphire.write_file(output_name=output_name, array=pt['array'], name_list=['stack_idx'], outlier_apply=pt['do_discard_outlier'], outlier_name=pt['outlier'])
        self.assertTrue(path.exists(NEW_INDEX_FILE_RAW) and path.isfile(NEW_INDEX_FILE_RAW))
        with open(NEW_INDEX_FILE_RAW, 'r') as read:
            lines = read.readlines()
        self.assertTrue(684 == len(lines))
        self.assertTrue(1 == len(lines[-1].split()))
        self.assertTrue('683\n' == lines[-1])
        clean_up(["new_index.txt"])

    def test_prepare_output(self):
        pt = self.generate_prior_tracker()
        self.assertTrue(self.output_file_index == ms_helix_sphire.prepare_output(tracker=pt['tracker'], file_name=NEW_INDEX_FILE_RAW,file_name_old=self.output_file_index))

    @classmethod
    def tearDownClass(cls):
        print "\n\tremove EMAN2DB folder"
        os_system("rm -r EMAN2DB/")

