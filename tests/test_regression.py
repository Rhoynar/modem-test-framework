import unittest
from helpers.helpers import *
from helpers.utils import *

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PythonDepsTestSuite))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DaemonsChecksTestSuite))
    unittest.TextTestRunner().run(suite)
    SystemChecksErrors.print_errors()
    Results.print_config()

