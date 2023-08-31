import json
import os
import time
import utils.logger_config as logger_config
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class GeneralTools:
    def __init__(self):
        pass

    def makeDirectory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def openJson(self):
        with open('utils\data.json') as json_file:
            return json.load(json_file)
            