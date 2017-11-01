# -*- coding: utf-8 -*-

import unittest
from system_checks import *
from utils import *

class DaemonsChecksTestSuite(unittest.TestCase):
    def test_required_services(self):
        ps_ef = run_cmd('ps -ef')
        assert 'ModemManager' in ps_ef
        if 'ModemManager' not in ps_ef:
            SystemChecksErrors.add_error('Modem Manager is not running. Start using: sudo start modemmanager')

        assert 'NetworkManager' in ps_ef
        if 'NetworkManager' not in ps_ef:
            SystemChecksErrors.add_error('Network Manager is not running. Start using: sudo start network-manager')

    def test_wwan_interfaces(self):
        ifcfg = run_cmd('ifconfig -a')
        assert 'wwan' in ifcfg
        if 'wwan' not in ifcfg:
            SystemChecksErrors.add_error('wwan interface is not enumerated. Please restart network-manager using: sudo stop network-manager && sudo start network-manager')

if __name__ == '__main__':
    unittest.main()
