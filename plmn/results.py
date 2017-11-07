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
        cls.state.clear()

    @classmethod
    def print_results(cls):
        logging.info('\n\n-------------------------------------------------------------------------------\n')
        logging.info('                                     RESULTS\n')
        logging.info('-------------------------------------------------------------------------------')
        if len(Results.state.keys()) > 0:
            logging.info('-------------------------------------------------------------------------------')
            logging.info(')                                     STATE')
            logging.info(pprint.pformat(Results.state))
            logging.info('-------------------------------------------------------------------------------')

        if len(Results.steps) > 0:
            logging.info('-------------------------------------------------------------------------------')
            logging.info(')                                     STEPS')
            for step in Results.steps:
                logging.info(step)
            logging.info('-------------------------------------------------------------------------------')

        if len(Results.errs) > 0:
            logging.info('-------------------------------------------------------------------------------')
            logging.info('                                      ERRORS')
            logging.info(' %30s | %s' % ('Command', 'Error Details'))
            for err in Results.errs:
                logging.info(' %30s | %s' % (err['cmd'], err['comment']))
            logging.info('-------------------------------------------------------------------------------')
        else:
            logging.info('-------------------------------------------------------------------------------')
            logging.info('                                    NO ERRORS!')
            logging.info('-------------------------------------------------------------------------------')

        logging.info('\n')
        cls.dump_results('test-results.json')



