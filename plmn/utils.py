import logging

# Setup debug variables.
_log_lvl = 'DEBUG'

# For minimal logging, use this setting:
# _log_lvl = 'DEBUG'


class MyFormatter(logging.Formatter):
    import datetime as dt

    converter = dt.datetime.fromtimestamp
    err_fmt  = "%(asctime)s | ERR | %(filename)s:%(lineno)s - %(funcName)20s(): %(message)s"
    dbg_fmt  = "%(asctime)s | DBG | %(filename)s:%(lineno)s - %(funcName)20s(): %(message)s"
    info_fmt = "%(message)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s

    def format(self, record):
        format_orig = self._fmt

        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = MyFormatter.err_fmt

        result = logging.Formatter.format(self, record)
        self._fmt = format_orig
        return result


# Decorator for running these functions only once.
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def setup_log_config():
    logFormatter = MyFormatter()
    rootLogger = logging.getLogger()
    rootLogger.setLevel(_log_lvl)

    # Open new file everytime
    fileHandler = logging.FileHandler("test.log", mode='w')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

def process_args():
    import argparse

    parser = argparse.ArgumentParser('PLMN Regression Test Cases')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug message to screen.')
    args, unknown = parser.parse_known_args()

    if args.debug:
        logFormatter = MyFormatter()
        rootLogger = logging.getLogger()
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
        logging.info(' ----------------------  RUNNING TESTS IN DEBUG MODE  ------------------------ ')

        # Return the number of arguments processed.
        return 1

    else:
        # Return indicating that no arguments were processed.
        return 0


# Setup logging subsystem.
setup_log_config()

if __name__ == '__main__':

    process_args()

    logging.info('Info message')
    logging.error('Error message')
    logging.debug('Debug Message')
