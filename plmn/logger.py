import logging

# Open fresh logging file each time.
with open('test.log', 'w'):
    pass

# Setup basic logging config.
logging.basicConfig(filename='test.log',level=logging.DEBUG)

# Setup various debug variables.
at_dbg = True
