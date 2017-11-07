# -*- coding: utf-8 -*-

import unittest
import compat
import sys
from plmn.network_checks import *

class NetworkRegisterVerizon(unittest.TestCase):
    def test_register_on_verizon(self):
        NetworkChecks.network_register('Verizon', 'vzwinternet')
        NetworkChecks.network_connect('Verizon', 'vzwinternet')

if __name__ == '__main__':
    nargs = process_args()
    unittest.main(argv=sys.argv[nargs:], exit=False)
    Results.print_results()
