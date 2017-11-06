# -*- coding: utf-8 -*-

import compat
import unittest

from plmn.results import *

from plmn.mmcli_helper import MMCLIHelper


class ModemChecks(unittest.TestCase):
    def test_mmcli_cmd_present(self):
        MMCLIHelper.mmcli_cmd_present()

    def test_list_modems(self):
        MMCLIHelper.list_modems()

    def test_modem_enabled(self):
        MMCLIHelper.modem_enabled()

    def test_modem_info(self):
        MMCLIHelper.modem_info()

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
