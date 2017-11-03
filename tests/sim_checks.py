# -*- coding: utf-8 -*-

import unittest
from utils import *
from mmcli_checks import MMCLIChecks

class SimChecks(unittest.TestCase):
    def test_sim_present(self):
        MMCLIChecks.sim_present()

    def test_sim_unlocked(self):
        MMCLIChecks.sim_unlocked()

    def test_sim_registered(self):
        MMCLIChecks.sim_registered()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
