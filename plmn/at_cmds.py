# -*- coding: utf-8 -*-

import unittest
import re
from modem_cmds import *

at_debug = True

class AtCmds():
    @classmethod
    def modem_sanity(cls):
        ModemCmds.modem_sanity()

    @classmethod
    def mm_debug_mode(cls):
        dbg_mode = ModemCmds.modem_manager_in_debug_mode()
        if dbg_mode is False:
            dbg_mode = ModemCmds.modem_manager_start_in_debug_mode()
        assert dbg_mode is True

    @classmethod
    def restart_mm_debug_mode(cls):
        cls.mm_debug_mode()

    @classmethod
    def send_at_cmd(cls, at_cmd, timeout=300):
        AtCmds.mm_debug_mode()

        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None
        cmd = "mmcli -m {} --command='{}' --timeout={}".format(modem_idx, at_cmd, timeout)

        res = Runner.run_cmd(cmd).strip()

        if at_debug:
            print "AT command: ", cmd
            print "Response: ", res

        res = res.replace('\r','|').replace('\n','|')
        match = re.search(r'response: \'(.*)\'', res)
        at_res = None
        if match is not None and match.group(1) is not None:
            at_res = match.group(1).strip()

        logging.info('Issuing AT command: {}, Response: \n{}'.format(cmd, at_res.replace('|', '\n')))
        return at_res

    @classmethod
    def unlock_at_cmds(cls):
        if True != Results.get_state('AT Unlocked'):
            res = cls.send_at_cmd('AT!ENTERCND="A710"')
            assert res == '', 'AT unlock command not succesful'
            Results.add_state('AT Unlocked', True)

    @classmethod
    def set_apn_name_in_profile(cls, pid=1, apn='broadband'):
        cls.mm_debug_mode()
        cls.unlock_at_cmds()

        res = cls.send_at_cmd('AT+CGDCONT?')
        assert res is not None

        res = cls.send_at_cmd('AT+CGDCONT={},"IP","{}"'.format(pid, apn))
        assert res is ''

        # Query again to check profile has been updated with new APN.
        res = cls.send_at_cmd('AT+CGDCONT?')
        assert res is not None
        assert apn in res

    @classmethod
    def perform_3gpp_scan(cls):
        AtCmds.mm_debug_mode()
        cls.unlock_at_cmds()

        # Check if network scan possible
        res = cls.send_at_cmd('AT+COPS?')
        assert res is not None

        # Perform Network Scan (default timeout of 300 sounds good)
        res = cls.send_at_cmd('AT+COPS=?')
        assert res is not None

    @classmethod
    def perform_auto_register(cls):
        cls.perform_3gpp_scan()

        res = cls.send_at_cmd('AT+COPS=0')
        assert res is not None

    @classmethod
    def perform_manual_register(cls, network_name='AT&T'):
        cls.perform_3gpp_scan()

        # For manually registering networks, make sure correct profile is present for them.
        if network_name == 'AT&T':
            cls.set_apn_name_in_profile(apn='broadband')
        elif network_name == 'Verizon':
            cls.set_apn_name_in_profile(apn='vzwinternet')
        elif network_name == 'T-Mobile':
            cls.set_apn_name_in_profile(apn='fast.t-mobile.com')
        else:
            # Add other network names and their APNs as needed.
            assert 0, 'Unknown network name to register on.'

        # Register manually on the given network.
        res = cls.send_at_cmd('AT+COPS=1,0,"{}"'.format(network_name))
        assert res is not None
