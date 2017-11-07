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

@run_once
def setup_log_config():
    logFormatter = MyFormatter()
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
