import json
import pprint

class Results:
    steps = []
    errs = []
    state = {}

    @classmethod
    def add_step(cls, cmd):
        Results.steps.append(cmd)

    @classmethod
    def add_error(cls, cmd, comment):
        Results.errs.append({'cmd' : cmd, 'comment': comment})

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
    def print_results(cls):
        print '\n\n-------------------------------------------------------------------------------\n'
        print '                                     RESULTS\n'
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
            print ' %20s | %s' % ('Command', 'Error Details')
            for err in Results.errs:
                print ' %20s | %s' % (err['cmd'], err['comment'])
            print '-------------------------------------------------------------------------------'

        print '\n'

        cls.dump_results('test-log.json')
