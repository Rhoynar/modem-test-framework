# -*- coding: utf-8 -*-

import compat
import unittest
import re

from plmn.logger import *
from plmn.results import *
from plmn.mmcli_helper import MMCLIHelper
from plmn.runner import *

class ModemChecks(unittest.TestCase):

    def setUp(self):
        MMCLIHelper.modem_sanity()
        # Check if modemmanager is in debug mode or socat application is installed.

    def _check_mm_debug_mode(self):
        # Check if modem manager is running in debug mode.
        debug_mode = MMCLIHelper.modem_manager_in_debug_mode()
        if debug_mode is False:
            MMCLIHelper.modem_manager_start_in_debug_mode()

        assert debug_mode is True

    def _send_at_cmd(self, at_cmd, timeout=300):
        self._check_mm_debug_mode()

        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None
        cmd = "mmcli -m {} --command='{}' --timeout={}".format(modem_idx, at_cmd, timeout)

        res = Runner.run_cmd(cmd).strip()
        res = res.replace('\r','|').replace('\n','|')
        match = re.search(r'response: \'(.*)\'', res)
        at_res = None
        if match is not None and match.group(1) is not None:
            at_res = match.group(1).strip()

        logging.info('Issuing AT command: {}, Response: \n{}'.format(cmd, at_res.replace('|', '\n')))
        return at_res

    def _unlock_at_cmds(self):
        self._check_mm_debug_mode()
        res = self._send_at_cmd('AT!ENTERCND="A710"')
        assert res == '', 'AT unlock command not succesful'
        Results.add_state('AT Unlocked', True)

    def set_apn_name_in_profile(self, pid=1, apn='broadband'):
        self._check_mm_debug_mode()
        self._unlock_at_cmds()

        res = self._send_at_cmd('AT+CGDCONT?')
        assert res is not None

        res = self._send_at_cmd('AT+CGDCONT={},"IP",{}'.format(pid, apn))
        assert res is ''

        # Query again to check profile has been updated with new APN.
        res = self._send_at_cmd('AT+CGDCONT?')
        assert res is not None
        assert apn in res

    def perform_3gpp_scan(self):
        self._check_mm_debug_mode()
        self._unlock_at_cmds()

        # Check if network scan possible
        res = self._send_at_cmd('AT+COPS?')
        assert res is not None

        # Perform Network Scan (default timeout of 300 sounds good)
        res = self._send_at_cmd('AT+COPS=?')
        assert res is not None

    def perform_auto_register(self):
        self.perform_3gpp_scan()

        res = self._send_at_cmd('AT+COPS=0')
        assert res is not None

    def perform_manual_register(self, network_name='AT&T'):
        self.perform_3gpp_scan()

        # For manually registering networks, make sure correct profile is present for them.
        if network_name == 'AT&T':
            self.set_apn_name_in_profile(apn='broadband')
        elif network_name == 'Verizon':
            self.set_apn_name_in_profile(apn='vzwinternet')
        elif network_name == 'T-Mobile':
            self.set_apn_name_in_profile(apn='fast.t-mobile.com')
        else:
            # Add other network names and their APNs as needed.
            assert 0, 'Unknown network name to register on.'

        # Register manually on the given network.
        res = self._send_at_cmd('AT+COPS=1,0,"{}"'.format(network_name))
        assert res is not None

    def test_modem_mgr_debug_mode(self):
        self._check_mm_debug_mode()

    def test_at_unlock(self):
        self._unlock_at_cmds()

    def test_at_basic_cmds(self):
        self._check_mm_debug_mode()
        self._unlock_at_cmds()

        # Check AT command version
        res = self._send_at_cmd('AT&V')
        assert res is not None

        # Check for model number
        res = self._send_at_cmd('AT+GMM')
        assert res is not None

        # Check for manufacturer
        res = self._send_at_cmd('AT+GMI')
        assert res is not None

        # Check modem capabilities.
        res = self._send_at_cmd('AT+GCAP')
        assert res is not None

        # Check current registration (manual or automatic)
        res = self._send_at_cmd('AT+COPS?')
        assert res is not None

        # Check modem firmware version.
        res = self._send_at_cmd('AT+CGMR')
        assert res is not None

        # Check supported registrations
        res = self._send_at_cmd('AT!SELRAT=?')
        assert res is not None

        # Check different PLMN profiles on modem.
        res = self._send_at_cmd('AT!SCACT?')
        assert res is not None

        # Check LTE Info
        res = self._send_at_cmd('AT!LTEINFO=?')
        assert res is not None
        assert 'Not Available' not in res

        # Check LTE NAS Info
        res = self._send_at_cmd('AT!LTENAS?')
        assert res is not None

        # Query Antenna settings configuration
        res = self._send_at_cmd('AT!ANTSEL=?')
        assert res is not None

        # Query Supported Bands.
        res = self._send_at_cmd('AT!BAND=?')
        assert res is not None

        # Query current band
        res = self._send_at_cmd('AT!GETBAND?')
        assert res is not None
        assert 'No Service' not in res, 'AT Command GETBAND reporting no service'

        # Query operational status
        res = self._send_at_cmd('AT!GSTATUS?')
        assert res is not None

        # Query Modem system indication mode.
        res = self._send_at_cmd('AT^MODE?')
        assert res is not None

        # Query Provisioned Network List.
        res = self._send_at_cmd('AT!NVPLMN?')
        assert res is not None

        # Query if PS (Packet Data Service) mode is enabled.
        res = self._send_at_cmd('AT!SELMODE?')
        assert res is not None
        assert 'PS' in res

        # Query currently configured profile details.
        res = self._send_at_cmd('AT+CGDCONT?')
        assert res is not None


    def test_at_3gpp_scan(self):
        self.perform_3gpp_scan()

    def test_at_auto_register(self):
        self.perform_auto_register()

    def test_at_manual_register(self):
        self.perform_manual_register('AT&T')

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
