

class SystemChecksErrors:
    errs = []

    @classmethod
    def add_error(cls, err):
        SystemChecksErrors.errs.append(err)

    @classmethod
    def print_errors(cls):
        if len(SystemChecksErrors.errs) > 0:
            print '\n\n'
            print '-------------------------------------------------------------'
            print 'Following errors were observed, please fix these and try again.'
            for err in SystemChecksErrors.errs:
                print '\n *** ERROR: ' + err
            print '-------------------------------------------------------------'
            print '\n\n'

class SystemChecks:
    # Basic Info
    python_exec = ''
    python_ver = ''
    python_ver_major = ''
    python_ver_minor = ''
    sudo_user = ''
    pip = ''
    pip_ver = ''

    # Modem Info
    modem_en = False
    modem_location = ''
    modem_idx = ''
    modem_man = ''
    modem_model = ''

    #
    supported_techs = []
    current_techs = []


    def __init__(self):
        pass

    @classmethod
    def print_config(cls):
        print ''
        print '-------------------------------------------------------------'
        print 'System Checks:'
        print 'Python:' + str(cls.python_exec)
        print 'Python Version: ' + str(cls.python_ver)
        print 'Sudo User: ' + str(cls.sudo_user)
        print '-------------------------------------------------------------'
