from time import sleep, gmtime
from random import randint
import calendar, json, ast, sys, yaml

input_lang = ['hindi', 'tamil', 'hindi', 'tamil', 'malayalam', 'konkani', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'marwari', 'marathi', 'marathi', 'marathi']
output_lang = ['english', 'telugu', 'oriya']

def reformat_log(log):
        json_acceptable_string = log.replace("'", "\"")
        json_log = json.loads(json_acceptable_string)
        json_log['time'] = str(calendar.timegm(gmtime()))
        print str(randint(0,len(input_lang) - 1))
        json_log['request']['RequestList']['ecomDataList']['olang'] = input_lang[randint(0,len(input_lang) - 1)]
        json_log['request']['tlangList'] = output_lang[randint(0,len(output_lang) - 1)]
        return json.dumps(json_log)

def random_sleep():
        sleep(0.2)

def parse_from_file():
        reader = open('test.log', 'r')
        writer = open('out.log', 'a', 0)
        for line in reader:
                random_sleep()
                formatted_log = reformat_log(line)
                writer.write(formatted_log)

parse_from_file()
