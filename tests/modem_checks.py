# -*- coding: utf-8 -*-

import unittest
import re
from utils import *
from mmcli_parser import MMCLIParser

class ModemChecks(unittest.TestCase):
    def mmcli_cmd_present(self):
        mmcli = run_cmd('which mmcli')
        if mmcli is None or len(mmcli.strip()) is 0:
            Results.add_error('which mmcli', 'mmcli is not present. Install modem manager using: sudo apt-get install modemmanager')
        else:
            Results.add_state('MMCLI Exec', mmcli.strip())

        mmcli_exec = Results.get_state('MMCLI Exec')
        if mmcli_exec is None:
            return False
        else:
            return True

    def test_mmcli_cmd_present(self):
        assert self.mmcli_cmd_present(), 'MMCLI command not present'

    def list_modems(self):
        if self.mmcli_cmd_present() is True:
            if Results.get_state('Modem Location') is None or Results.get_state('Modem Index') is None:
                mmcli = run_cmd('mmcli -L')
                if '/org/freedesktop/ModemManager' not in mmcli:
                    Results.add_error('mmcli -L', 'Modem not found. Please enable the modem through instrument UI.')
                else:
                    Results.add_state('Modem Location', re.search(r'(/org/freedesktop/ModemManager\d/Modem/\d)', mmcli).group(1))
                    Results.add_state('Modem Index', re.search(r'/org/freedesktop/ModemManager\d/Modem/(\d)', Results.get_state('Modem Location')).group(1))

        modem_loc = Results.get_state('Modem Location')
        modem_idx = Results.get_state('Modem Index')
        return modem_loc is not None and modem_idx is not None

    def test_list_modems(self):
        self.mmcli_cmd_present()
        assert self.list_modems(), 'Modems cannot be listed.'

    def test_modem_enabled(self):
        self.mmcli_cmd_present()
        self.list_modems()

        modem_idx = Results.get_state('Modem Index')
        mmcli = run_cmd('mmcli -m {} --simple-status'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if res is not None and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'disabled':
            Results.add_error('mmcli -m {} --simple-status'.format(modem_idx), 'Modem not enabled. Please enable using mmcli -m {} --enable'.format(modem_idx))

        if res is not None and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            Results.add_state('Modem Enabled', True)
        else:
            Results.add_error('mmcli -m {} --simple-status'.format(modem_idx), 'Modem not registered. Contact support with log files')

    def test_modem_info(self):
        self.mmcli_cmd_present()
        self.list_modems()

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

    def sim_present(self):
        self.list_modems()

        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] != 'failed':
            Results.add_state('SIM Present', True)
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not found. Fix Insert SIM card and restart modem')

    def test_sim_present(self):
        self.sim_present()

    def test_sim_registered(self):
        self.sim_present()

        # Modem not present, no need to run this test.
        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None

        sim_present = Results.get_state('SIM Present')
        assert sim_present is not None

        mmcli = run_cmd('mmcli -m {}'.format(modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            Results.add_state('SIM Registered', True)
            return True
        else:
            Results.add_error('mmcli -m {}'.format(modem_idx), 'SIM card not registered. Please restart modem manager using: sudo stop modemmanager && sudo start modemmanager')
            return False

if __name__ == '__main__':
    unittest.main(exit=False)
    Results.print_results()
