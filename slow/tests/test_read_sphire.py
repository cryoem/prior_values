import sys
sys.path.append('modules')
sys.path.append('.')
import os as os
import sparx as sp
import numpy as np
import read_sphire

class TestReadSphire():
    def test_get_sphire_stack_length(self):
        """Test if the length of the sphire stack is correct"""
        stack_name = 'bdb:stack_small'
        return_array = read_sphire.get_sphire_stack(stack_name)
        print(len(return_array))
        print(return_array[0])
        assert(len(return_array) == 684)


