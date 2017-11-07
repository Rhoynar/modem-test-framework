import unittest

import at_checks
import daemons_check
import modem_checks
import python_checks
import sim_checks

from plmn.results import *

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Add all regression test-cases to this test-suite.
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(python_checks.PythonChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(daemons_check.DaemonChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(modem_checks.ModemChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(at_checks.AtCmdChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(sim_checks.SimChecks))

    # Run the regression suite.
    unittest.TextTestRunner().run(suite)

    # Print final system state.
    Results.print_results()
