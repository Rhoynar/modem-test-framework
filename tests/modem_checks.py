# -*- coding: utf-8 -*-

import unittest
from results import Results
from utils import *
import re
from mmcli_parser import MMCLIParser
import json

class ModemChecksTestSuite(unittest.TestCase):
    def test_mmcli_cmd_present(self):
        mmcli = run_cmd('which mmcli')
        if len(mmcli) is 0:
            Results.add_error('which mmcli', 'mmcli is not present. Install modem manager using: sudo apt-get install modemmanager')
        else:
            Results.add_state('MMCLI Exec', mmcli)

    def test_list_modems(self):
        # MMCLI not present, skip running other tests.
        mmcli_exec = Results.get_state('MMCLI Exec')
        if mmcli_exec is None:
            return

        mmcli = run_cmd('mmcli -L')
        if '/org/freedesktop/ModemManager' not in mmcli:
            Results.add_error('mmcli -L', 'Modem not found. Please enable the modem through instrument UI.')

        else:
            Results.add_state('Modem Location', re.search(r'(/org/freedesktop/ModemManager\d/Modem/\d)', mmcli).group(1))
            Results.add_state('Modem Index', re.search(r'/org/freedesktop/ModemManager\d/Modem/(\d)', Results.get_state('Modem Location')).group(1))

    def test_sim_present(self):
        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] != 'failed':
            Results.add_state('SIM Present', True)
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not found. Fix Insert SIM card and restart modem')

    def test_sim_registered(self):
        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return

        sim_present = Results.get_state('SIM Present')
        if sim_present is None or sim_present is False:
            return

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            Results.add_state('SIM Registered', True)
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not registered. Please restart modem manager using: sudo stop modemmanager && sudo start modemmanager')

    def test_get_modem_info(self):
        modem_idx = Results.get_state('Modem Index')
        if modem_idx is None:
            return

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if len(res.keys()) > 0:
            Results.add_state('Modem Info', res)
            assert 'Hardware' in res.keys()
            assert 'System' in res.keys()
            assert 'Numbers' in res.keys()
            assert 'Bands' in res.keys()
            assert 'IP' in res.keys()
            assert 'SIM' in res.keys()
            assert '3GPP' in res.keys()
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'Error getting/parsing modem info. Contact support with test output.')

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
