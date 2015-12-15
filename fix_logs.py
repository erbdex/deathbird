#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import sleep
from random import randint
import json, sys


def fix_log_timestamp(time_in_log):
    # Converting time to a second epoch.
    epoch = time_in_log / 1000
    return epoch

def fix_nested_objects(json_log):
    '''
        Flattening request object nested within array so that Kibana can micro-analyse it.
        Doesn't do it for docs like- [{...},{...}]
        See- https://github.com/elastic/kibana/issues/998
    '''
    json_log['request']['RequestList'][0]['ecomDataList'] = json_log['request']['RequestList'][0]['ecomDataList'][0]
    json_log['request']['RequestList'] = json_log['request']['RequestList'][0]
    json_log['request']['tlangList'] = json_log['request']['tlangList'][0]

    json_log['response']['map']['data']['myArrayList'] = json_log['response']['map']['data']['myArrayList'][0]['myArrayList'][0]
    return json_log


def extract_json_from_log(log):
    # The logged line is-- "2015-12-11 08:17:34 - {..valid..json..}\n"
    delimiter = '- '
    return log.split(delimiter)[1]



def reformat_log(logged_line):
    log = extract_json_from_log(logged_line)
    json_acceptable_string = log.replace("'", "\"")
    json_log = dict()
    try:
        json_log = json.loads(json_acceptable_string)

        # The log right now logs the second epoch with the last three ms digits appended. Translates to ~47000 AD.
        timestamp_logged = json_log['time']
        json_log['time'] = fix_log_timestamp(timestamp_logged)

        # Flattening request object nested within array so that Kibana can micro-analyse it.
        fixed_log = fix_nested_objects(json_log)
    except Exception as e:
        print 'Error: \"{0}\" Trace: \"{1}\"'.format(log, e)

    return json.dumps(fixed_log)


def random_sleep():
    sleep(0.01 * randint(0, 50))


def parse_from_file():
    reader = open(sys.argv[1], 'r')
    writer = open(sys.argv[2], 'a', 0)
    try:
        reader.seek(0)
        for line in reader:
             random_sleep()
             formatted_log = reformat_log(line)
             print formatted_log
             writer.write(formatted_log + '\n')
    except Exception as e:
        print 'Raised: {0}'.format(e)

if __name__ == '__main__':
    parse_from_file()
