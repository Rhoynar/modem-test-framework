# -*- coding: utf-8 -*-

import compat
import unittest

from plmn.utils import *
from plmn.results import *
from plmn.modem_cmds import *
from plmn.simple_cmds import *

class SimpleCmdChecks(unittest.TestCase):
    def test_simple_status_cmd(self):
        SimpleCmds.simple_status_cmd()
        assert Results.get_state('Simple Status') is not None

    def test_simple_status_get_reg_status(self):
        SimpleCmds.simple_status_get_reg_status()

    def test_simple_status_is_registered(self):
        assert SimpleCmds.simple_status_is_registered() is True

    def test_simple_status_is_home(self):
        assert SimpleCmds.simple_status_is_home() is True
        assert SimpleCmds.simple_status_is_roaming() is False

    @unittest.skip('Skipping this test since this is only applicable in connected state')
    def test_simple_status_is_connected(self):
        assert SimpleCmds.simple_status_is_connected() is True

    @unittest.skip('Skipping this as this is only applicable for Roaming scenario')
    def test_simple_status_is_roaming(self):
        assert SimpleCmds.simple_status_is_roaming() is True


if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
