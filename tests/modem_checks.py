# -*- coding: utf-8 -*-

import unittest
from system_checks import *
from utils import *
import re
from mmcli_parser import MMCLIParser
import json

class ModemChecksTestSuite(unittest.TestCase):
    def test_mmcli_cmd_present(self):
        mmcli = run_cmd('which mmcli')
        assert len(mmcli) > 0
        if len(mmcli) is 0:
            SystemChecksErrors.add_error('mmcli is not present. Install modem manager using: sudo apt-get install modemmanager')

    def test_list_modems(self):
        mmcli = run_cmd('mmcli -L')
        assert '/org/freedesktop/ModemManager' in mmcli
        if '/org/freedesktop/ModemManager' not in mmcli:
            SystemChecksErrors.add_error('Modem not found. Please enable the modem through instrument UI.')
        SystemChecks.modem_location = re.search(r'(/org/freedesktop/ModemManager\d/Modem/\d)', mmcli).group(1)
        SystemChecks.modem_idx = re.search(r'/org/freedesktop/ModemManager\d/Modem/(\d)', SystemChecks.modem_location).group(1)

    def test_sim_present(self):
        # Modem not present, no need to run this test as same error is returned from list_modems.
        if SystemChecks.modem_idx == -1:
            return

        mmcli = run_cmd('mmcli -m {}'.format(SystemChecks.modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            SystemChecks.modem_en = True
        else:
            SystemChecksErrors.add_error('SIM card not found/registered. Fix SIM issue and restart modem.')
            assert 0

    def test_modem_enabled(self):
        mmcli = run_cmd('mmcli -m {} --simple-status'.format(SystemChecks.modem_idx))
        res = MMCLIParser.parse(mmcli)
        if 'Status' in res.keys() and 'state' in res['Status'].keys() and res['Status']['state'] == 'registered':
            SystemChecks.modem_en = True
        else:
            SystemChecksErrors.add_error('Modem not enabled. Please enable modem using: mmcli -m {} --enable'.format(SystemChecks.modem_idx))
            assert 0

    def test_get_modem_info(self):
        if SystemChecks.modem_idx == -1:
            return

        mmcli = run_cmd('mmcli -m {}'.format(SystemChecks.modem_idx))
        res = MMCLIParser.parse(mmcli)
        assert 'Hardware' in res.keys()
        assert 'System' in res.keys()
        assert 'Numbers' in res.keys()
        assert 'Bands' in res.keys()
        assert 'IP' in res.keys()
        assert 'SIM' in res.keys()
        assert '3GPP' in res.keys()
        SystemChecks.modem_info = res

    def test_wwan_interfaces(self):
        ifcfg = run_cmd('ifconfig -a')
        assert 'wwan' in ifcfg
        if 'wwan' not in ifcfg:
            SystemChecksErrors.add_error('wwan interface is not enumerated. Please restart network-manager using: sudo stop network-manager && sudo start network-manager')

if __name__ == '__main__':
    unittest.main(exit=False)
    print 'outputting json file.'
    with open('test.json', 'w') as json_file:
        json.dump(SystemChecks.modem_info, json_file, indent=4)

    with open('test2.json', 'w') as json_file:
        json.dump(SystemChecksErrors.errs, json_file, indent=4)
