# -*- coding: utf-8 -*-

import unittest

from plmn.utils import *

from plmn.helpers import MMCLIHelper


class SimChecks(unittest.TestCase):
    def test_sim_present(self):
        MMCLIHelper.sim_present()

    def test_sim_unlocked(self):
        MMCLIHelper.sim_unlocked()

    def test_sim_registered(self):
        MMCLIHelper.sim_registered()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
