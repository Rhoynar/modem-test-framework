PLMN Regression Project. Implements the following test plan.

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