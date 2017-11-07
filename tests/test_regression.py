import unittest

import at_checks
import daemons_check
import modem_checks
import python_checks
import sim_checks
import simple_cmd_checks

from plmn.utils import *
from plmn.results import *

if __name__ == '__main__':
    process_args()

    suite = unittest.TestSuite()

    # Add all regression test-cases to this test-suite.
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(python_checks.PythonChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(daemons_check.DaemonChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(modem_checks.ModemChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(at_checks.AtCmdChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(sim_checks.SimChecks))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(simple_cmd_checks.SimpleCmdChecks))

    # Run the regression suite.
    unittest.TextTestRunner().run(suite)

    # Print final system state.
    Results.print_results()
