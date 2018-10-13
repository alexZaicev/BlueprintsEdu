import logging
import os, sys
import re

ROOT_PATH = re.search('(.*)BlueprintsApp', os.path.dirname(os.path.abspath(__file__))).group(1)
LOG_DIR = "BlueprintsApp\logs\\"
LOG_FILENAME = "BlueprintApp.log"
PATH = ROOT_PATH + LOG_DIR

if not os.path.exists(PATH):
    try:
        os.makedirs(PATH)
    except OSError as ex:
        raise Exception("Failed to create log directory")

logging.basicConfig(filename=(PATH+LOG_FILENAME), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
