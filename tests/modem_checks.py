# -*- coding: utf-8 -*-

import unittest
import re
import json

from utils import *
from helpers import *
from mmcli_parser import MMCLIParser
from results import Results


class ModemChecks(unittest.TestCase):
    def mmcli_cmd_present(self):
        mmcli = run_cmd('which mmcli')
        if len(mmcli) is 0:
            Results.add_error('which mmcli', 'mmcli is not present. Install modem manager using: sudo apt-get install modemmanager')
            return False
        else:
            Results.add_state('MMCLI Exec', mmcli)
            return True


    def list_modems(self):
        # MMCLI not present, skip running other tests.
        mmcli_exec = Results.get_state('MMCLI Exec')
        if mmcli_exec is None:
            return False

        mmcli = run_cmd('mmcli -L')
        if '/org/freedesktop/ModemManager' not in mmcli:
            Results.add_error('mmcli -L', 'Modem not found. Please enable the modem through instrument UI.')
            return False

        else:
            Results.add_state('Modem Location', re.search(r'(/org/freedesktop/ModemManager\d/Modem/\d)', mmcli).group(1))
            Results.add_state('Modem Index', re.search(r'/org/freedesktop/ModemManager\d/Modem/(\d)', Results.get_state('Modem Location')).group(1))
            return True

    def sim_present(self):
        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return False

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] != 'failed':
            Results.add_state('SIM Present', True)
            return True
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not found. Fix Insert SIM card and restart modem')
            return False

    def sim_registered(self):
        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return False

        sim_present = Results.get_state('SIM Present')
        if sim_present is None or sim_present is False:
            return False

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            Results.add_state('SIM Registered', True)
            return True
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not registered. Please restart modem manager using: sudo stop modemmanager && sudo start modemmanager')
            return False

    def modem_info(self):
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return False

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if len(res.keys()) > 0:
            Results.add_state('Modem Info', res)
            return True
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'Error getting/parsing modem info. Contact support with test output.')
            return False

    def test_modem_checks(self):
        assert self.mmcli_cmd_present() is True
        assert self.list_modems() is True
        assert self.sim_present() is True
        assert self.sim_registered() is True
        assert self.modem_info() is True

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
