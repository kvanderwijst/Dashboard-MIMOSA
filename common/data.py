###################
#
# Common data functions
#
###################

import glob
import pandas as pd

DATA_DIRECTORY = 'outputdata\\'


# Get all available experiments
def get_all_experiments():
    filenames = glob.glob(DATA_DIRECTORY+('output_*.csv'))
    return filenames


class DataStore:

    databases = {}

    def __init__(self):
        pass

    def reset(self):
        self.databases = {}

    def get(self, filename, force_new=False):
        # 1. Check if file still needs to be read out
        if filename not in self.databases or force_new:
            self.databases[filename] = read_content(filename)
        # 2. Return database from cache
        return self.databases[filename]

dataStore = DataStore()


# Read content of file, together with parameters
def read_content(filename):

    try:
        # First strip all slashes 
        filename = filename.replace('/','').replace('\\','')

        content = pd.read_csv(DATA_DIRECTORY+filename)
    except:
        return None

    return content