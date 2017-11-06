# -*- coding: utf-8 -*-

import unittest
import time
import tests.compat
from plmn.results import *
from plmn.modem_cmds import ModemCmds
from plmn.runner import *
from plmn.at_cmds import *

class NetworkChecks():

    @classmethod
    def _network_register_using_at(cls, network_name, apn_name):
        # Modem sanity
        AtCmds.modem_sanity()

        # Restart modem-manager in debug mode if needed.
        AtCmds.mm_debug_mode()

        # Unlock all at-commands.
        AtCmds.unlock_at_cmds()

        # Update default profile with correct APN name.
        AtCmds.set_apn_name_in_profile(1, apn_name)

        # Perform 3GPP scan
        AtCmds.perform_3gpp_scan()

        # Perform manual register
        # AtCmds.perform_manual_register(network_name)

        # Perform auto-register.
        AtCmds.perform_auto_register()

    @classmethod
    def network_register(cls, network_name, apn_name):
        cls._network_register_using_at(network_name, apn_name)

if __name__ == '__main__':
    NetworkChecks.network_register('AT&T', 'broadband')
