# PLMN Regression Project

This project implements a number of test cases that provide a regression framework for checking modem status, registration and connectivity. 

## Test Plan

This project implements the following test plan is implemented.
* Basic System Checks:
    * Check if sudo access is available for the user and application.
    * Check if Python is available and print its version (2.7+ should be supported)
    * Check if all python package requirements are satisfied (PySerial etc).
    * Check if modem manager is running.
    * Check if network manager is running.
    * Check if wwan interfaces are available and enumerated (part of ifconfig -a)
    * Check what is the interface to be used for AT commands.
    * Check if LAN interface is available and can be used to reach outside world.
* Modem Existence Checks:
    * Check if modem is present
    * Check if modem is enabled
    * Print the name, model number of the modem.
    * Print Modem Capabilities
    * Check if SIM card is present in the modem
    * Check if SIM card is unlocked and can be used.
* AT Command Pre-reqs:
    * Check if Modem Manager is running in debug mode or if socat application is present. Set AT runner to mmcli or socat
    * Check if extended AT commands set can be unlocked using the password
    * Check if basic AT commands like AT+GMM etc are running correctly.
* Network Checks (mmcli and AT commands):
    * Check if modem is registered on a network. (simple-status)
    * Check if a 3GPP scan can be performed to list out all available networks.
    * <Roaming only> Check to see if modem can be forced to register to other networks.
    * Force automatic registration at the end to bring modem to good state.
* Data Call Checks
    * Bring up default data call in automatic registration mode. Use nmcli commands to bring up corresponding interfaces. Perform data transfer over this interface.
    * <Roaming only> Bring up data call over a different registration. Use nmcli commands to bring up the interface. Perform data transfer over this interface. 
    * Tear Down the data call. Verify interface is brought down.
    * Repeated data call bring-up.
    * Check and report Data Transfer speeds [uplink and downlink]
    

## How to Use
The following steps show the various ways to use this project.

* Options supported with all types of runs:

    We can specify ``--debug`` option with all the test cases and registration runs.

* Running Individual Test Cases

    Run individual test cases by running them through the console directly.

    ```python modem_checks.py``` 

    Or run with debug option:

    ```python modem_checks.py --debug``

* Running Regression Test Suite:
    
    We can run all the regression tests in one go by running the regression python module.

    ```python test_regression.py``

* Running Registration Scenarios:

    Registration scenarios are not included in regression as they are end-to-end scenario and do not belong with unit test cases. You can run registration commands by running the appropriate module:

    ```python network_register_atnt.py --debug```


## Project Layout and Overview
The project is divided into two main folders: ***plmn*** - which implement different features, functionalities and helper routines; and ***tests*** - which implement different test cases and scenarios.

### ***plmn***
The plmn folder consists of different modules for implementing features and functionalities required for this project.

* **runner.py**:

    The runner.py file implements **Runner** class which allows to run a specific MMCLI command through subprocess call. It uses subprocess python call and pipes to capture the standard output or errors. This class exports a single class **Runner** which provides a static method: ``Runner.run_cmd(cmd)``. This is implemented as a static method to allow callers to call this without instantiating any object.

* **results.py**

    The results.py file implements the **Results** class which maintains the state of execution. The main objective of **Results** class is to maintain a state of different operations performed, what were the errors observed, what is the modem state at the end of execution. The following variables in **Results** class indicate the overall state. Since there is a single state at the end of execution, this class is impelemented through static variables and methods.

    * State Variables in **Results**
        * **steps[]** : Maintains a list of steps or commands executed.
        * **errs[]**: Maintains a list of errors in Results.
        * **state{}**: Maintains different state variables of Results. This contains a dictionary of values and consists of parsed command outputs for ``mmcli -m 0`` and ``mmcli -m 0 --simple-status`` commands.

    * Methods available in **Results**
        * ``add_state(state, val)``: Add a state to the Results. state is a string attribute and val can be any value: string, integer, boolean or a dictionary object.
        * ``get_state(state)``: Return the value maintained by identifier ``state``. ``state`` is a string indicating which state to get.
        * ``add_step(step)``: Add a step that was recently executed to the state.
        * ``add_error(cmd, comment)``: If any command indicated error after execution, add the error message along with any additional comments on how to resolve this error through comments.
        * ``print_results()``: Prints the state of results in a human readable format. It will internally dump the results to a JSON file as well.

* **mmcli_parser.py**

    The ``mmcli_parser.parse()`` method parses the output provided by any MMCLI command and translates it into a Python dictionary object. The mmcli command output, when successful, consists of tabulated, 3 column. We translate it into Python dictionary object. For example the following line is an output from MMCLI list command:

    ``"Hardware |   manufacturer: 'Sierra Wireless, Incorporated'"``

    This is translated into following Python object ``state``:

    ```
    {
        Hardware : 
        {
            manufacturer: "Sierra Wireless, Incorporated"
        }
    }
    ```

* **utils.py**

    This file provides various utility functionalities for rest of the modules. They include:
    * **Logging** : We use an internal logging formatter to allow us to format different types log messages. Info messages are usually used for printing state messages and don't have a time/date/filename pre-fix to them. Debug messages and error messages do include a time/date/filename prefix.

    * **Argument Parsing**: Most of the runners use unittest test cases, so we have to capture and parse known command line arguments before handing over rest of arguments to the unittest module. We do that through argparse module which is implemented in this file.

    * **Running with ``--debug`` Option**: We can run any of the test cases or entry points for this project using ``--debug`` argument. This allows us to observe the progress of the project in real time as all the logs are printed to screen console.

    * **Logging output**: All log messages (debug, info, errors and any exceptions observed) are logged directly to **test.log** file which would be generated in the tests directory. We also generate a **test-results.json** file which contains the status of ``Results`` state.

* **modem_cmds.py**: 

    This file contains all the functions related to various modem MMCLI commands. All methods are implemented as static methods and can be run by using ``ModemCmds.method_name()``

    * ``mmcli_cmd_present()`` : Check if mmcli command is available.
    * ``list_modems()``: List different modems available using ``mmcli -L`` command.
    * ``list_modem_wait()``: This is a blocking function which waits till a modem becomes available. This is useful in cases of a modem restart - this waits till the modem becomes available and returns when it has been listed.
    * ``modem_enabled()``: This method checks if the modem is enabled (if it is in "enabled", "registered" or "connected" states)
    * ``modem_info()``: Get all modem info using ``mmcli -m 0`` command. Parse all results into a python object and store it in results.
    * ``sim_present()``: Checks if a SIM card is available.
    * ``sim_unlocked()``: Checks if a SIM card is unlocked.
    * ``is_sim_registered()``: Returns if a SIM card is "registered" or "connected" state.
    * ``sim_registered()``: This method asserts if a SIM card is registered.
    * ``modem_manager_is_running()``: This method checks to see if the modem manager daemon is running.
    * ``modem_manager_in_debug_mode()``: This function checks if the modem manager is running in debug mode (with ``--debug`` options.). Most AT commands need the modem manager to run in debug mode.
    * ``modem_manager_start_in_debug_mode()``: This function checks if the modem manager is running in debug mode, if not it starts the modem manager in debug mode.
    * ``modem_sanity()``: This performs few sanity checks on the modem.
    * ``modem_lpm_online()``: This performs a modem soft cycle: which means it puts modem in low-power mode and enables the modem again. Similar to putting modem in Air Plane mode and back online.

* **network_checks.py**

    This file provides methods to perform network registration and connect to a APN. The idea is that this module will be used by carrier specific test cases (listed below) in order to initiate a registration/connection routine on a specific carrier.

    * ``network_register(network_name, apn)``: This method implements a network register routine from start to finish. Usually used after hot-swapping a SIM card, this would trigger all tricks in the book in order for the SIM card to quickly register on a particular network. There are differences in ways CDMA networks such as Verizon operate (support auto-connect on registration) vs other networks (like AT&T which require we explicitly connect). This method hides all those details internally and provides a simple, easy-to-use external interface that can be replicated in an app.

    * ``network_connect(network_name, apn)``: This method performs network connection after registration. Please note that network_register() should be called before this method.

* **simple_cmds.py**

    This file contains wrapper methods for executing various ``simple`` commands that mmcli supports. Commands such as ``--simple-status`` and ``--simple-connect`` are supported.

    * ``modem_sanity()``: Checks for modem sanity before performing any commands.
    * ``simple_status_cmd()``: Wrapper around ``mmcli -m 0 --simple-status`` command.
    * ``simple_status_get_reg_status()``: Run simple-status command and check the registration status.
    * ``simple_status_is_registered()``: Run simple-status command and return True if registered or connected.
    * ``simple_status_is_connected()``: Run simple-status command and return True if connected.
    * ``simple_status_is_roaming()``: Run simple-status command to figure out if modem is roaming or on home network.
    * ``simple_connect()``: Connect to a network using mmcli simple commands.

* **at_cmds.py**

    This file contains wrappers for executing various AT commands to the modem. We use mmcli as an interface to talk to the modem. In order for most of the AT commands to work, there are two pre-requisites.

    * Modem Manager must be running in debug mode. There is a method in this class ``AtCmds.restart_mm_debug_mode()`` which will restart the modem manager daemon in debug mode if it is not running in debug mode already.

    * Extended AT commands should be unlocked. Majority of the AT commands used herein fall under "Extended AT commands" category. In order to unlock these commands, we need to send **AT!ENTERCND="A710"** command to the modem. There is a wrapper method in this module ``AtCmds.unlock_at_cmds`` which performs unlocking for us.

    Following methods are exported through this module.

    * ``restart_mm_debug_mode()``: Restart modem manager in debug mode.
    * ``send_at_cmd()``: Send an AT command. Default timeout of 300 seconds is used. Timeout is worse case time for the command, in most cases, the command will complete well before the timeout.
    * ``unlock_at_cmds()``: This method performs an unlock of the Extended AT command set. This needs to be called only once prior to sending any extended AT commands.
    * ``set_apn_name_in_profile()``: This method sets the APN name specified in the modem profile. This is required, even for registration, on networks such as Verizon which support auto-connect on register.
    * ``perform_3gpp_scan()``: Uses ``AT+COPS=?`` to perform a network scan. This is simpilar in operation to ``mmcli -m 0 --3gpp-scan``
    * ``perform_auto_register()``: Uses ``AT+COPS=0`` to trigger an automatic registration request to the modem.
    * ``perform_manual_register()``: Uses ``AT+COPS=1,0,"AT&T"`` to trigger a registration request on a specified network name. Network name is obtained from ``perform_3gpp_scan()`` method from above.
    * ``restart_modem()``: This command restarts the modem using the AT command: ``AT!GRESET`` command. After the modem is restarted, this performs a polling wait till the modem is listed again through MMCLI commands.


### ***tests***

This module lists all test cases supported for PLMN regression. 

* Regression Tests
    * **compat.py** : This file is a utility file that allows the test cases to be run from tests directory as well from main root directory.
    * **at_checks.py** : This file implements all the AT command regression test cases.
    * **daemons_checks.py** : This file implements checking if modem manager and network manager daemons are running, are they in debug modes etc.
    * **modem_checks.py**: This file checks different modem checks needed. Such as whether modem is listed, modem is enabled, getting modem info etc.
    * **python_checks.py**: This file checks whether python, pip and all its dependencies is available in the system. 
    * **sim_checks.py**: This file checks for all SIM checks. Whether SIM card is present or not, whether sim card is enabled and unlocked and whether SIM card is registered on a network.
    * **simple_cmd_checks.py**: This file tests for different simple-commands such as simple-status and simple-connect.
    * **test_regression.py**: This is a single regression module that runs all the above test cases. It creates a test-suite, adds all modules to the test suite, creates a text test runner and runs all the test suites.

* Network Registration Cycles:
    * **network_register_atnt.py**: This module perform complete registration on a AT&T SIM card. This creates the correct profile based on the network name and triggers a restart followed by registration process for AT&T.    
    * **network_register_verizon.py**: This module perform complete registration on a Verizon SIM card. This creates the correct profile based on the network name and triggers a restart followed by registration process for Verizon.


