# -*- coding: utf-8 -*-

import unittest
from system_checks import *
from utils import *
import re

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

    def test_modem_enabled(self):
        mmcli = run_cmd('mmcli -m {} --simple-status'.format(SystemChecks.modem_idx))
        if "state: 'disabled'" in mmcli:
            SystemChecksErrors.add_error('Modem not enabled. Please enable modem using: mmcli -m {} --enable'.format(SystemChecks.modem_idx))
        assert 'enabled' in mmcli
        SystemChecks.modem_en = True

    def test_get_modem_info(self):
        mmcli = run_cmd('mmcli -m {}'.format(SystemChecks.modem_idx))

        man = re.search("manufacturer: '(.+)'$", mmcli)
        assert man is not None and man.group(1) is not None
        if man is None or man.group(1) is None:
            SystemChecksErrors.add_error('Modem manufacturer cannot be parsed.')
        SystemChecks.modem_manu = man.group(1)

        model = re.search("model: '(.+)'$", mmcli)
        assert model is not None and model.group(1) is not None
        if model is None or model.group(1) is None:
            SystemChecksErrors.add_error('Modem model number cannot be parsed.')
        SystemChecks.modem_model = model.group(1)


    def test_get_modem_capabilities(self):
        mmcli = run_cmd('mmcli -m {}'.format(SystemChecks.modem_idx))

        # Find supported techs.
        hardware_start = mmcli.find('Hardware') + len('Hardware')
        hardware = mmcli[hardware_start:]
        hardware_end = hardware.find('-------------------------')
        hardware = hardware[:hardware_end]

        supported_start = hardware.find('supported:') + len('supported:')
        supported_end = hardware.find('current:')
        supported = hardware[supported_start:supported_end]
        SystemChecks.supported_techs = re.findall(r'[a-z0-9\-]+', supported.lower())

        # Find current techs.
        current_start = hardware.find('current:') + len('current:')
        current = hardware[current_start:]
        SystemChecks.current_techs = re.findall(r'[a-z0-9\-]+', current.split('\n')[0])

    def test_wwan_interfaces(self):
        ifcfg = run_cmd('ifconfig -a')
        assert 'wwan' in ifcfg
        if 'wwan' not in ifcfg:
            SystemChecksErrors.add_error('wwan interface is not enumerated. Please restart network-manager using: sudo stop network-manager && sudo start network-manager')

if __name__ == '__main__':
    unittest.main()
