# -*- coding: utf-8 -*-

import unittest
import time
import tests.compat
from plmn.utils import *
from plmn.results import *
from plmn.modem_cmds import ModemCmds
from plmn.runner import *
from plmn.at_cmds import *
from plmn.simple_cmds import *

class NetworkChecks():

    @classmethod
    def _network_register_using_at(cls, network_name, apn_name):
        # Modem sanity
        ModemCmds.modem_sanity()

        # Restart modem-manager in debug mode if needed.
        AtCmds.mm_debug_mode()

        # Unlock all at-commands.
        AtCmds.unlock_at_cmds()

        # Update default profile with correct APN name.
        AtCmds.set_apn_name_in_profile(1, apn_name)

        # Restart Modem. (put in Low Power mode and back online)
        AtCmds.restart_modem()

        for idx in range(0, 5):
            # Perform LPM/Online if still not registered.
            sim_reg = ModemCmds.is_sim_registered()
            if sim_reg is False:
                ModemCmds.mode_lpm_online()

            # Perform auto-register.
            sim_reg = ModemCmds.is_sim_registered()
            if sim_reg is False:
                AtCmds.perform_auto_register()

            # Perform 3GPP scan and try auto-register again.
            sim_reg = ModemCmds.is_sim_registered()
            if sim_reg is False:
                AtCmds.perform_3gpp_scan()
                AtCmds.perform_auto_register()

            if sim_reg is True:
                break

        # Perform manual register
        # AtCmds.perform_manual_register(network_name)


        # Ensure modem is registered now.
        ModemCmds.modem_enabled()
        ModemCmds.sim_registered()

    @classmethod
    def network_register(cls, network_name, apn_name):
        cls._network_register_using_at(network_name, apn_name)

    @classmethod
    def network_connect(cls, network_name, apn_name):
        SimpleCmds.simple_connect(apn_name)

if __name__ == '__main__':
    NetworkChecks.network_register('AT&T', 'broadband')
