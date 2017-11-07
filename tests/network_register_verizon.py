# -*- coding: utf-8 -*-

import unittest
import compat
from plmn.network_checks import *

class NetworkRegisterVerizon(unittest.TestCase):
    def test_register_on_verizon(self):
        NetworkChecks.network_register('Verizon', 'vzwinternet')
        NetworkChecks.network_connect('Verizon', 'vzwinternet')

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
