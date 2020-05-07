import json
import time


class JsonTool:

    @staticmethod
    def parse(filename):
        with open(filename, 'r+') as f:
            #time.sleep(1)
            return json.loads(f.read())

    @staticmethod
    def save_to_file(filename, data):
        with open(filename, 'w') as f:
            #time.sleep(1)
            #print(data)
            f.write(json.dumps(data))
            #f.write('\n')