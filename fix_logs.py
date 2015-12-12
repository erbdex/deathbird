
from time import sleep
import json, ast, sys, yaml

def reformat_log(log):
	json_acceptable_string = log.replace("'", "\"")
	json_log = json.loads(json_acceptable_string)
	json_log['time'] = '1449940902'
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
