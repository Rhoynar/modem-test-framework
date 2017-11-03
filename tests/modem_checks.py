# -*- coding: utf-8 -*-

import unittest
from utils import *
from mmcli_checks import MMCLIChecks

class ModemChecks(unittest.TestCase):
    def test_mmcli_cmd_present(self):
        MMCLIChecks.mmcli_cmd_present()

    def test_list_modems(self):
        MMCLIChecks.list_modems()

    def test_modem_enabled(self):
        MMCLIChecks.modem_enabled()

    def test_modem_info(self):
        MMCLIChecks.modem_info()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
