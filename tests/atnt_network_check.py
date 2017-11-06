# -*- coding: utf-8 -*-

import unittest
import compat
from plmn.network_checks import *

class AtntNetworkChecks(unittest.TestCase):
    def test_register_on_atnt(self):
        NetworkChecks.network_register('AT&T', 'broadband')

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
