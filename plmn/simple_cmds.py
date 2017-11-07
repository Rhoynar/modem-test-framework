# -*- coding: utf-8 -*-

import unittest
import re
from modem_cmds import *

class SimpleCmds():
    @classmethod
    def modem_sanity(cls):
        ModemCmds.modem_sanity()


    @classmethod
    def simple_status_cmd(cls):
        cls.modem_sanity()

        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None

        cmd = "mmcli -m {} --simple-status".format(modem_idx)
        res = Runner.run_cmd(cmd).strip()

        if cmd_dbg:
            print "Response: ", res

        simple_status = MMCLIParser.parse(res)
        assert simple_status is not {}

        Results.add_state('Simple Status', simple_status)


    @classmethod
    def simple_status_get_reg_status(cls):
        cls.simple_status_cmd()
        simple_status = Results.get_state('Simple Status')
        return simple_status['Status']['state']

    @classmethod
    def simple_status_is_registered(cls):
        return cls.simple_status_get_reg_status() == 'registered' or cls.simple_status_get_reg_status() == 'connected'

    @classmethod
    def simple_status_is_connected(cls):
        return cls.simple_status_get_reg_status() == 'connected'

    @classmethod
    def simple_status_is_home(cls):
        if cls.simple_status_is_registered():
            simple_status = Results.get_state('Simple Status')
            if simple_status['3GPP']['registration'] == 'home':
                return True
        return False

    @classmethod
    def simple_status_is_roaming(cls):
        if cls.simple_status_is_registered():
            simple_status = Results.get_state('Simple Status')
            if simple_status['3GPP']['registration'] == 'roaming':
                return True
        return False

    @classmethod
    def _simple_connect(cls, apn):
        modem_idx = Results.get_state('Modem Index')
        assert modem_idx is not None

        cmd = 'mmcli -m {} --simple-connect="apn={}"'.format(modem_idx, apn)
        res = Runner.run_cmd(cmd).strip()

        time.sleep(2)

        cls.simple_status_cmd()

    @classmethod
    def simple_connect(cls, apn):
        if cls.simple_status_is_connected():
            if cmd_dbg:
                print 'Modem is already connected!'
        elif cls.simple_status_is_registered():
            if cmd_dbg:
                print 'Modem is registered on network. Connecting using APN: ' + apn
            cls._simple_connect(apn)
            assert cls.simple_status_is_connected()
        else:
            assert 0, 'Modem not registered, cannot perform simple-connect'
