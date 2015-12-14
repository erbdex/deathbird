from time import sleep, gmtime
from random import randint, choice
import calendar, json, ast, sys, yaml

input_lang = 'hindi', 'tamil', 'hindi', 'tamil', 'malayalam', 'konkani', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'bhojpuri', 'punjabi', 'marwari', 'marathi', 'marathi', 'marathi'
output_lang = 'english', 'telugu', 'oriya', 'english', 'english', 'english', 'urdu', 'urdu', 'urdu', 'bengali'
api_keys = '44615f2b6ddbc6228c254673148ac0425642', '44615f2b6ddbc6228c254673148ac0425642', 'cf2bc00a6caafdacbac53d59ad214ef08f80', 'cf2bc00a6caafdacbac53d59ad214ef08f80', '2c358efbae4c0a7f35be91a0a2ec06f7b2ab', '2c358efbae4c0a7f35be91a0a2ec06f7b2ab', '2c358efbae4c0a7f35be91a0a2ec06f7b2ab', '2c358efbae4c0a7f35be91a0a2ec06f7b2ab', '2c358efbae4c0a7f35be91a0a2ec06f7b2ab', '709e4fcd7df7ef1f8cc5a860afc7ca7fc7c3', 'e0cf8c563d5d1de9ad3bfbffc4ac3f902ff1', '4a4dd6549e777b5fffebe0d63131ee56f81a', '056c7f80f6fd7ac4cba2aca429dc94bf0f5b', 'f540ac51bcccdc1065f159af9eef382a50db', '88fe888d0b693eb5ab5fca7aefe94ac5a6cd', '7fe412e62ecfb2a9ca3766319b192eeb90be', '7fe412e62ecfb2a9ca3766319b192eeb90be', '7fe412e62ecfb2a9ca3766319b192eeb90be', '7fe412e62ecfb2a9ca3766319b192eeb90be', '7fe412e62ecfb2a9ca3766319b192eeb90be'


'''
"data": {
          "myArrayList": [
            {
              "myArrayList": [
                {
                  "map": {
                    "loc_val": {
                      "map": {
                        "hindi": "ऍब्सोल्यूट मार्ट ब्लैक हाइ हील्ड पम्पस"
                      }
                    },
                    "loc_attr": {
                      "map": {
                        "hindi": "शीर्षक"
                      }
                    },
                    "attr": "title",
                    "value": "Absolute Mart Black High Heeled Pumps"
                  }
                }
              ]
            }
          ]
        }



"data": {
          "myArrayList": {
            "map": {
              "loc_val": {
                "map": {
                  "hindi": "ऍब्सोल्यूट मार्ट ब्लैक हाइ हील्ड पम्पस"
                }
              },
              "loc_attr": {
                "map": {
                  "hindi": "शीर्षक"
                }
              },
              "attr": "title",
              "value": "Absolute Mart Black High Heeled Pumps"
            }
          }
        }

'''


def reformat_log(log):
        rand_api_key = choice(api_keys)
        json_acceptable_string = log.replace("'", "\"")
        json_log = json.loads(json_acceptable_string)
        json_log['time'] = str(calendar.timegm(gmtime()))
        json_log['request']['RequestList'][0]['ecomDataList'][0]['olang'] = choice(input_lang)
        json_log['request']['tlangList'] = choice(output_lang)
        json_log['request']['apiKey'] = rand_api_key
        json_log['apikey'] = rand_api_key
        json_log['response']['map']['apikey'] = rand_api_key
        print '.',
        sys.stdout.flush()
        return json.dumps(json_log)

def random_sleep():
        sleep(0.01 * randint(0, 50))

def parse_from_file():
        reader = open('clean_logs.log', 'r')
        writer = open('test.log', 'a', 0)
        while True:
            reader.seek(0)
            for line in reader:
                 random_sleep()
                 formatted_log = reformat_log(line)
                 writer.write(formatted_log + '\n')

parse_from_file()
