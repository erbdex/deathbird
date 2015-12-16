import json, time, random, traceback, sys

class ReverieParser():
    def __init__(self):
        pass

    def fix_log_timestamp(self, time_in_log):
        # Converting time to a second epoch.
        epoch = time_in_log / 1000
        return epoch

    def fix_nested_objects(self, json_log):
        '''
            Flattening request object nested within array so that Kibana can micro-analyse it.
            Doesn't do it for docs like- [{...},{...}] See- https://github.com/elastic/kibana/issues/998
        '''
        json_log['request']['RequestList'][0]['ecomDataList'] = json_log['request']['RequestList'][0]['ecomDataList'][0]
        json_log['request']['RequestList'] = json_log['request']['RequestList'][0]
        json_log['request']['tlangList'] = json_log['request']['tlangList'][0]

        json_log['response']['map']['data']['myArrayList'] = json_log['response']['map']['data']['myArrayList'][0]['myArrayList'][0]
        return json_log

    def extract_json_from_log(self, log):
        # The logged line is-- "2015-12-11 08:17:34 - {..valid..json..}\n"
        if log[-1:] == '\n':
            log.rstrip()

        delimiter = '- '
        return log.split(delimiter)[1]


    def reformat_log(self, logged_line):
        log = self.extract_json_from_log(logged_line)
        json_acceptable_string = log.replace("'", "\"")
        json_log = fixed_log = dict()
        try:
            json_log = json.loads(json_acceptable_string)

            # The log right now logs the second epoch with the last three ms digits appended. Translates to ~47000 AD.
            timestamp_logged = json_log['time']
            json_log['time'] = self.fix_log_timestamp(timestamp_logged)

            # Flattening request object nested within array so that Kibana can micro-analyse it.
            fixed_log = self.fix_nested_objects(json_log)
        except Exception as e:
            print 'Error: \"{0}\" Trace: \"{1}\"'.format(log, e)
            traceback.print_exc(file=sys.stdout)


        return json.dumps(fixed_log)


    def reverie_sleep(self):
        time.sleep(0.01 * random.randint(0, 50))

    def test_format(self, log):
        return log