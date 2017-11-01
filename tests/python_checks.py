import unittest
import subprocess
import re
import os
from system_checks import *
from utils import *

class PythonDepsTestSuite(unittest.TestCase):
    def test_python_location(self):
        python_exec = run_cmd('which python')
        if len(python_exec) is 0:
            SystemChecksErrors.add_error('Python not installed. Please install python using: sudo apt-get install python2.7')
        SystemChecks.python_exec = python_exec.strip()

    def test_python_version(self):
        python_ver = run_cmd('python --version')
        python_ver_major = re.findall(r'[0-9]+', python_ver)[0]
        python_ver_minor = re.findall(r'[0-9]+', python_ver)[1]
        # Suite is developed with Python 2.7+ in mind.
        if int(python_ver_major) != 2 or int(python_ver_minor) < 7:
            SystemChecksErrors.add_error('Python 2.7+ version not present. Please install latest python 2.7 using: sudo apt-get install python2.7')
        SystemChecks.python_ver = python_ver.strip()
        SystemChecks.python_ver_major = python_ver_major.strip()
        SystemChecks.python_ver_minor = python_ver_minor.strip()

    def test_user_name(self):
        username = os.getenv('SUDO_USER')
        assert username is not None
        if username is None:
            SystemChecksErrors.add_error('Program needs to be run with sudo permissions.')
        SystemChecks.sudo_user = username

    def test_pip(self):
        pip = run_cmd('which pip')
        assert len(pip) > 0
        if len(pip) == 0:
            SystemChecksErrors.add_error('Python Package Manager (PIP) not present. Please install using: sudo apt-get install python-pip')
        SystemChecks.pip = pip.strip()

    def test_pip_version(self):
        pip_ver = run_cmd('pip --version')
        pip_ver_major = re.findall(r'[0-9]+', pip_ver)[0]

        assert int(pip_ver_major) >= 9
        if int(pip_ver_major) < 9:
            SystemChecksErrors.add_error('Incorrect PIP version found. Please install latest pip using: sudo apt-get install python-pip')
        SystemChecks.pip_ver = pip_ver.strip()

    def test_pip_pacakages(self):
        # Check if required pip packages exist
        pip_pkgs = run_cmd('pip freeze')

        # For now pyserial is the only required package,
        # others may be required in future.
        assert 'pyserial' in pip_pkgs.lower()
        if ('pyserial' not in pip_pkgs.lower()):
            SystemChecksErrors.add_error('PySerial package not found. Please install using: pip install pyserial')


if __name__ == '__main__':
    unittest.main()
