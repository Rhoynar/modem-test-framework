# -*- coding: utf-8 -*-

import compat
import unittest

from plmn.results import *

from plmn.modem_cmds import ModemCmds


class ModemChecks(unittest.TestCase):
    def test_mmcli_cmd_present(self):
        ModemCmds.mmcli_cmd_present()

    def test_list_modems(self):
        ModemCmds.list_modems()

    def test_modem_enabled(self):
        ModemCmds.modem_enabled()

    def test_modem_info(self):
        ModemCmds.modem_info()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
