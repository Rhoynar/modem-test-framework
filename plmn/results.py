from utils import *
import json
import pprint

class Results:
    steps = []
    errs = []
    state = {}

    @classmethod
    def add_step(cls, cmd):
        step_already_added = False
        for step in Results.steps:
            if step == cmd:
                step_already_added = True
                break
        if not step_already_added:
            Results.steps.append(cmd)

    @classmethod
    def add_error(cls, cmd, comment):
        err_already_added = False
        for err in Results.errs:
            if err['cmd'] == cmd and err['comment'] == comment:
                err_already_added = True

        if err_already_added == False:
            Results.errs.append({'cmd' : cmd, 'comment': comment})
            logging.error('Error in ' + cmd + ', Details: ' + comment)
            assert 0, comment

    @classmethod
    def add_state(cls, state, val):
        Results.state[state] = val

    @classmethod
    def get_state(cls, key):
        if key in Results.state.keys():
            return Results.state[key]
        else:
            return None

    @classmethod
    def dump_results(cls, filename):
        res = { 'state' : Results.state, 'steps' : Results.steps, 'errors' : Results.errs }
        with open(filename, 'w') as json_file:
            json.dump(res, json_file, indent=4)

    @classmethod
    def reset(cls):
        logging.info('Reset state.')
        cls.state = {}

    @classmethod
    def print_results(cls):
        print '\n\n-------------------------------------------------------------------------------\n'
        print '                                    RESULTS\n'
#        print '                                    ---------'
        print '-------------------------------------------------------------------------------'
        if len(Results.state.keys()) > 0:
            print '-------------------------------------------------------------------------------'
            print '                                     STATE'
            pprint.pprint(Results.state)
            print '-------------------------------------------------------------------------------'

        if len(Results.steps) > 0:
            print '-------------------------------------------------------------------------------'
            print '                                     STEPS'
            for step in Results.steps:
                print step
            print '-------------------------------------------------------------------------------'

        if len(Results.errs) > 0:
            print '-------------------------------------------------------------------------------'
            print '                                     ERRORS'
            print ' %30s | %s' % ('Command', 'Error Details')
            for err in Results.errs:
                print ' %30s | %s' % (err['cmd'], err['comment'])
            print '-------------------------------------------------------------------------------'
        else:
            print '-------------------------------------------------------------------------------'
            print '                                    NO ERRORS!'
            print '-------------------------------------------------------------------------------'

        print '\n'

        cls.dump_results('test-results.json')



