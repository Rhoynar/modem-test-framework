# -*- coding: utf-8 -*-

import unittest
import compat
from plmn.results import *
from plmn.modem_cmds import ModemCmds


class SimChecks(unittest.TestCase):
    def test_sim_present(self):
        ModemCmds.sim_present()

    def test_sim_unlocked(self):
        ModemCmds.sim_unlocked()

    def test_sim_registered(self):
        ModemCmds.sim_registered()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
