# -*- coding: utf-8 -*-

import compat
import unittest

from plmn.utils import *
from plmn.mmcli_helper import MMCLIHelper

class ModemChecks(unittest.TestCase):

    def setUp(self):
        MMCLIHelper.modem_sanity()
        # Check if modemmanager is in debug mode or socat application is installed.

    def test_modem_mgr_debug_mode(self):
        # Add test for checking debug mode.
        pass

    def test_at_socat(self):
        pass
        # Add test for checking socat application

    def test_at_unlock(self):
        pass
        # Add test for unlocking AT commands.

    def test_at_basic_cmds(self):
        pass
        # Add test for basic AT commands like AT+GMM

    def test_at_3gpp_scan(self):
        pass
        # Add test to scan for networks.

    def test_at_auto_register(self):
        pass
        # Register automatically on network.

    def test_at_manual_register(self):
        pass
        # Register automatically on network.


if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
