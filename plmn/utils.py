import logging

# Setup debug variables.
_console_dbg = True
_log_lvl = 'DEBUG'

# For minimal logging, use this setting:
# _console_dbg = False
# _log_lvl = 'DEBUG'

# Open fresh logging file each time.
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def setup_log_config():
    # print 'Clearing test.log file'
    # with open('test.log', 'w'):
    #     pass

    _log_format = "%(filename)s:%(lineno)s - %(funcName)20s(): %(message)s"
    logFormatter = logging.Formatter(_log_format)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(_log_lvl)

    # Open new file everytime
    fileHandler = logging.FileHandler("test.log", mode='w')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    if _console_dbg:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

# Setup logging subsystem.
setup_log_config()

if __name__ == '__main__':
    logging.info('Info message')
    logging.error('Error message')
    logging.debug('Debug Message')
