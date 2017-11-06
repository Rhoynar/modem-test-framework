import logging

# Open fresh logging file each time.
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def clear_log_file():
    if cmd_dbg:
        print 'Clearing test.log file'
    with open('test.log', 'w'):
        pass


# Setup basic logging config.
clear_log_file()
logging.basicConfig(filename='test.log',level=logging.DEBUG)

# Setup various debug variables.
at_dbg = True
cmd_dbg = True