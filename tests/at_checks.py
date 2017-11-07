# -*- coding: utf-8 -*-

import compat
import unittest
import re

from plmn.utils import *
from plmn.results import *
from plmn.modem_cmds import ModemCmds
from plmn.runner import *
from plmn.at_cmds import *

class AtCmdChecks(unittest.TestCase):

    def setUp(self):
        AtCmds.modem_sanity()
        # Check if modemmanager is in debug mode or socat application is installed.

    def test_modem_mgr_debug_mode(self):
        AtCmds.mm_debug_mode()

    def test_at_unlock(self):
        AtCmds.unlock_at_cmds()

    def test_at_basic_cmds(self):
        AtCmds.mm_debug_mode()
        AtCmds.unlock_at_cmds()

        # Check AT command version
        res = AtCmds.send_at_cmd('AT&V')
        assert res is not None

        # Check for model number
        res = AtCmds.send_at_cmd('AT+GMM')
        assert res is not None

        # Check for manufacturer
        res = AtCmds.send_at_cmd('AT+GMI')
        assert res is not None

        # Check modem capabilities.
        res = AtCmds.send_at_cmd('AT+GCAP')
        assert res is not None

        # Check current registration (manual or automatic)
        res = AtCmds.send_at_cmd('AT+COPS?')
        assert res is not None

        # Check modem firmware version.
        res = AtCmds.send_at_cmd('AT+CGMR')
        assert res is not None

        # Check supported registrations
        res = AtCmds.send_at_cmd('AT!SELRAT=?')
        assert res is not None

        # Check different PLMN profiles on modem.
        res = AtCmds.send_at_cmd('AT!SCACT?')
        assert res is not None

        # Check LTE Info
        res = AtCmds.send_at_cmd('AT!LTEINFO=?')
        assert res is not None

        # Check LTE NAS Info
        res = AtCmds.send_at_cmd('AT!LTENAS?')
        assert res is not None

        # Query Antenna settings configuration
        res = AtCmds.send_at_cmd('AT!ANTSEL=?')
        assert res is not None

        # Query Supported Bands.
        res = AtCmds.send_at_cmd('AT!BAND=?')
        assert res is not None

        # Query current band
        res = AtCmds.send_at_cmd('AT!GETBAND?')
        assert res is not None
        assert 'No Service' not in res, 'AT Command GETBAND reporting no service'

        # Query operational status
        res = AtCmds.send_at_cmd('AT!GSTATUS?')
        assert res is not None

        # Query Modem system indication mode.
        res = AtCmds.send_at_cmd('AT^MODE?')
        assert res is not None

        # Query Provisioned Network List.
        res = AtCmds.send_at_cmd('AT!NVPLMN?')
        assert res is not None

        # Query if PS (Packet Data Service) mode is enabled.
        res = AtCmds.send_at_cmd('AT!SELMODE?')
        assert res is not None
        assert 'PS' in res

        # Query currently configured profile details.
        res = AtCmds.send_at_cmd('AT+CGDCONT?')
        assert res is not None


    @unittest.skip('Skip 3GPP scanning. Enable this for manual run.')
    def test_at_3gpp_scan(self):
        AtCmds.perform_3gpp_scan()

    @unittest.skip('Skip Auto Register. Enable this for manual run.')
    def test_at_auto_register(self):
        AtCmds.perform_auto_register()

    @unittest.skip('Skip Manual Register Test on a given Network for regression. Enable this for manual run.')
    def test_at_manual_register(self):
        AtCmds.perform_manual_register('AT&T')

if __name__ == '__main__':
    process_args()
    unittest.main(exit=False)
    Results.print_results()
