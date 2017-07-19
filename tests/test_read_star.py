import sys
sys.path.append('modules')
sys.path.append('.')
import os as os
import sparx as sp
import numpy as np
import read_star

class TestReadStar():
    def test_create_dtype_dict(self):
        dtype_dict = read_star.create_dtype_dict()
        assert(isinstance(dtype_dict, dict))


    def test_import_star_file_length_data(self):
        file_name = 'data_test.star'
        data, header, path = read_star.import_star_file(file_name)
        assert(len(data) == 274)


    def test_import_star_file_length_header(self):
        file_name = 'data_test.star'
        data, header, path = read_star.import_star_file(file_name)
        assert(len(header) == 31)


    def test_import_star_file_path(self):
        file_name = 'data_test.star'
        data, header, path = read_star.import_star_file(file_name)
        assert(file_name == path)

