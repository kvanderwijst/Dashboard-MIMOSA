###################
#
# Common data functions
#
###################

import glob
import json
import os.path
import pandas as pd


DATA_DIRECTORY = 'outputdata'

def filename_to_path(filename):
    # Strip filename of slashes for security
    filename = filename.replace('/','').replace('\\','')
    return os.path.join(os.path.dirname(__file__), '..', DATA_DIRECTORY, filename)


# Get all available experiments
def get_all_experiments():
    paths = glob.glob(filename_to_path('output_*.csv'))
    return [os.path.os.path.basename(path) for path in paths]


class DataStore:

    databases = {}
    params = {}

    def __init__(self):
        pass

    def reset(self):
        self.databases = {}
        self.params = {}

    def get(self, filename, force_new=False):
        # 1. Check if file still needs to be read out
        if filename not in self.databases or force_new:
            self.databases[filename] = read_content(filename)
        # 2. Return database from cache
        return self.databases[filename]

    def getparams(self, filename, force_new=False):
        # 1. Check if param file exists and still needs to be read out
        if filename not in self.params or force_new:
            self.params[filename] = read_param(filename)
        # 2. Return param dict from cache
        return self.params[filename]


dataStore = DataStore()


# Read content of file
def read_content(filename):

    try:
        # First strip all slashes 
        filename = filename.replace('/','').replace('\\','')

        content = pd.read_csv(filename_to_path(filename))
    except:
        return None

    return content


# Read content of parameter
def read_param(filename):

    try:
        # First strip all slashes 
        filename = filename.replace('/','').replace('\\','') + '.params.json'

        with open(filename_to_path(filename), 'r') as f:
            content = json.load(f)

    except:
        return None

    return content