import ms_helix_sphire
import unittest
from os import system as os_system


RELATIVE_PATH_EMAN2= "../../EMAN2DB"
NAME = 'bdb:stack'
INDEX_FILE_RAW = '../tests/index_raw.txt'
PARAMS_FILE_RAW = '../tests/params_raw.txt'


class Test_ms_helix_sphire(unittest.TestCase):
    SKIP_TEST = False

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
        print "test"

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
        pass

    def test_write_index_file(self):
        pass

    def test_write_file(self):
        pass

    def test_prepare_output(self):
        pass


    @classmethod
    def tearDownClass(cls):
        print "\n\tremove EMAN2DB folder"
        os_system("rm -r EMAN2DB/")

