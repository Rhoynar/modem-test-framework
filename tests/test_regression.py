import unittest
from daemons_check import *
from python_checks import *
from system_checks import *

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PythonDepsTestSuite))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DaemonsChecksTestSuite))
    unittest.TextTestRunner().run(suite)
    SystemChecksErrors.print_errors()
    SystemChecks.print_config()

