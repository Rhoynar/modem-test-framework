# -*- coding: utf-8 -*-

import unittest
import re
from modem_cmds import *

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
    def _try_3gpp_scan(cls, timeout=300):

        for idx in range(0,3):
            modem_idx = Results.get_state('Modem Index')
            assert modem_idx is not None
            cmd = "mmcli -m {} --3gpp-scan --timeout {}".format(modem_idx, timeout + 100*idx)

            logging.debug("3GPP Scan command: " + str(cmd))
            res = Runner.run_cmd(cmd).strip()
            logging.debug("Response: \n" + str(res))

            if "couldn't scan networks in the modem" not in res:
                break


    @classmethod
    def _try_send_at_cmd(cls, at_cmd, timeout):
        AtCmds.mm_debug_mode()

        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None
        cmd = "mmcli -m {} --command='{}' --timeout={}".format(modem_idx, at_cmd, timeout)

        logging.debug("AT command: " + str(cmd))
        res = Runner.run_cmd(cmd).strip()
        logging.debug("Response: \n" + str(res))

        res = res.replace('\r','|').replace('\n','|')
        match = re.search(r'response: \'(.*)\'', res)
        at_res = None
        if match is not None and match.group(1) is not None:
            at_res = match.group(1).strip()

        return at_res

    @classmethod
    def send_at_cmd(cls, at_cmd, timeout=300):
        at_res = cls._try_send_at_cmd(at_cmd, timeout)
        if at_res is None:
            for idx in range(0,2):
                time.sleep(1)
                # Some error occurred in AT command processing. Retry (upto 3 times)
                at_res = cls._try_send_at_cmd(at_cmd, timeout)
                if at_res is not None:
                    break

        assert at_res is not None
        return at_res

    @classmethod
    def unlock_at_cmds(cls):
        if True != Results.get_state('AT Unlocked'):
            res = cls.send_at_cmd('AT!ENTERCND="A710"')
            logging.debug("AT Unlock Results: " + str(res))
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
        res = cls._try_3gpp_scan()
        assert res is not None

    @classmethod
    def perform_auto_register(cls):
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

    @classmethod
    def restart_modem(cls):
        ModemCmds.list_modem_wait()
        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None

        cls.unlock_at_cmds()
        res = cls.send_at_cmd('AT!GRESET')
        time.sleep(5)

        Results.reset()
        ModemCmds.list_modem_wait()
