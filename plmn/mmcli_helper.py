# -*- coding: utf-8 -*-

import re

from utils import *
from cmd_runner import MMCLIRunner
from mmcli_parser import MMCLIParser

class MMCLIHelper:
    @classmethod
    def mmcli_cmd_present(cls):
        mmcli_exec = Results.get_state('MMCLI Exec')
        if mmcli_exec is None:
            mmcli_exec = MMCLIRunner.run_cmd('which mmcli')
            if mmcli_exec is not None and len(mmcli_exec.strip()) is 0:
                Results.add_state('MMCLI Exec', mmcli_exec.strip())

        assert mmcli_exec is not None

    @classmethod
    def list_modems(cls):
        cls.mmcli_cmd_present()

        modem_loc = Results.get_state('Modem Location')
        if modem_loc is None:
            mmcli = MMCLIRunner.run_cmd('mmcli -L')
            if '/org/freedesktop/ModemManager' not in mmcli:
                Results.add_error('mmcli -L', 'Modem not found. Please enable the modem through instrument UI.')
            else:
                modem_loc = re.search(r'(/org/freedesktop/ModemManager\d/Modem/\d)', mmcli.strip()).group(1)
                Results.add_state('Modem Location', modem_loc)
                Results.add_state('Modem Index', re.search(r'/org/freedesktop/ModemManager\d/Modem/(\d)', modem_loc).group(1))
        assert modem_loc is not None

    @classmethod
    def modem_enabled(cls):
        cls.list_modems()

        modem_en = Results.get_state('Modem Enabled')
        if modem_en is None:
            modem_idx = Results.get_state('Modem Index')
            mmcli = MMCLIRunner.run_cmd('mmcli -m {} --simple-status'.format(modem_idx))
            res = MMCLIParser.parse(mmcli)
            if res is not None and 'Status' in res.keys() and 'state' in res['Status'].keys():
                if res['Status']['state'] == 'disabled':
                    Results.add_error('mmcli -m {} --simple-status'.format(modem_idx), 'Modem not enabled. Please enable using mmcli -m {} --enable'.format(modem_idx))

                elif res['Status']['state'] != 'registered':
                    Results.add_error('mmcli -m {} --simple-status'.format(modem_idx),
                                      'Modem not registered. Contact support with log files')
                else:
                    modem_en = True
                    Results.add_state('Modem Enabled', modem_en)

        assert modem_en is True

    @classmethod
    def modem_info(cls):
        cls.list_modems()

        modem_info = Results.get_state('Modem Info')
        if modem_info is None:
            modem_idx = Results.get_state('Modem Index')
            assert modem_idx is not None

            mmcli = MMCLIRunner.run_cmd('mmcli -m {}'.format(modem_idx)).strip()
            modem_info = MMCLIParser.parse(mmcli)
            if len(modem_info.keys()) > 0:
                Results.add_state('Modem Info', modem_info)
            else:
                Results.add_error('mmcli -m {}'.format(modem_idx),
                                  'Error getting/parsing modem info. Contact support with test output.')

        assert modem_info is not None

    @classmethod
    def sim_present(cls):
        cls.list_modems()

        sim_present = Results.get_state('SIM Present')
        if sim_present is None:
            modem_idx = Results.get_state('Modem Index')
            mmcli = MMCLIRunner.run_cmd('mmcli -m {}'.format(modem_idx))
            res = MMCLIParser.parse(mmcli)
            if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys():
                if res['Status']['state'] == 'failed':
                    Results.add_error('mmcli -m {}'.format(modem_idx) + ' | gerp state',
                                      'SIM card not found. Insert SIM card and restart modem')
                else:
                    sim_present = True
                    Results.add_state('SIM Present', sim_present)

        assert sim_present is True

    @classmethod
    def sim_unlocked(cls):
        cls.sim_present()

        sim_unlocked = Results.get_state('SIM Unlocked')
        if sim_unlocked is None:
            modem_idx = Results.get_state('Modem Index')
            assert modem_idx is not None

            mmcli = MMCLIRunner.run_cmd('mmcli -m {}'.format(modem_idx))
            res = MMCLIParser.parse(mmcli)
            if '3GPP' in res.keys() and 'enabled locks' in res['3GPP'].keys():
                if res['3GPP']['enabled locks'] == 'none':
                    sim_unlocked = True
                    Results.add_state('SIM Unlocked', sim_unlocked)
                else:
                    Results.add_state('SIM Unlocked', False)
                    Results.add_error('mmcli -m {}'.format(modem_idx) + ' | grep \'enabled lock\'', 'SIM card is locked with a PIN.')
        assert sim_unlocked is True

    @classmethod
    def sim_registered(cls):
        cls.sim_present()
        cls.sim_unlocked()

        sim_registered = Results.get_state('SIM Registered')
        if sim_registered is None:
            modem_idx = Results.get_state('Modem Index')
            assert modem_idx is not None

            mmcli = MMCLIRunner.run_cmd('mmcli -m {}'.format(modem_idx))
            res = MMCLIParser.parse(mmcli)
            if 'SIM' in res.keys() and 'Status' in res.keys() and 'state' in res['Status'].keys():
                if res['Status']['state'] == 'registered':
                    sim_registered = True
                    Results.add_state('SIM Registered', sim_registered)
                else:
                    Results.add_state('SIM Registered', False)
                    Results.add_error('mmcli -m {}'.format(modem_idx) + ' | grep state',
                                      'SIM card not registered. Please restart modem manager using: sudo stop modemmanager && sudo start modemmanager')

        assert sim_registered is True

    @classmethod
    def modem_sanity(cls):
        cls.mmcli_cmd_present()
        cls.modem_enabled()
        cls.sim_registered()
