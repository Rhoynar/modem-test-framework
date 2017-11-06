# -*- coding: utf-8 -*-

import unittest
import time
import compat
from plmn.results import *
from plmn.mmcli_helper import MMCLIHelper
from plmn.runner import *
from at_checks import *


class NetworkChecks():

    @classmethod
    def _network_register_using_at(cls, network_name, apn_name):
        # Restart modem-manager in debug mode.
        at_runner = AtCmdChecks()
        at_runner.restart_mm_in_debug_mode()

        # Unlock all at-commands.
        at_runner.unlock_at_cmds()

        # Update default profile with correct APN name.
        at_runner.set_apn_name_in_profile(1, apn_name)

        # Perform 3GPP scan
        at_runner.perform_3gpp_scan()

        # Perform manual register
        at_runner.perform_manual_register(network_name)

        # Perform auto-register.
        at_runner.perform_auto_register()

    @classmethod
    def network_register(cls, network_name, apn_name):
        cls._network_register_using_at(network_name, apn_name)

if __name__ == '__main__':
    NetworkChecks.network_register('AT&T', 'broadband')
