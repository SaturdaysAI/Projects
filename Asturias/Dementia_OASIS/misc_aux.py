import pandas as pd
import pickle
import bz2
import _pickle as cPickle


def getDataFrameFromDict(dict):
    properties = ['ID', 'M/F', 'Hand', 'Age', 'Educ', 'SES',
                  'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF', 'Delay', 'Dementia']
    subset = [[value['1'][prop] for prop in properties]
              for key, value in dict.items()]
    return pd.DataFrame(subset, columns=properties)


def dropparameters(dataframe, keys=[]):
    d2 = dataframe
    for key in keys:
        d2 = d2.drop(key, axis=1)
    return d2


def parse_hyperconstraints_line(line):
    # Remove comments
    line = line.split('#')[0].strip()
    if not line:
        return None

    # Split the line into key and values
    key, values = line.split(':', 1)
    key = key.strip()
    values = values.split(',')

    parsed_values = []
    for value in values:
        value = value.strip()
        # Try parsing as int
        try:
            parsed_value = int(value)
        # If not int, try parsing as float
        except ValueError:
            try:
                parsed_value = float(value)
            # If not float, consider it as string
            except ValueError:
                parsed_value = value
        parsed_values.append(parsed_value)

    # Extract low_value, high_value, step (optional), extraparam (optional)
    if len(parsed_values) >= 2:
        low_value = parsed_values[0]
        high_value = parsed_values[1]
        step = parsed_values[2] if len(parsed_values) > 2 else None
        extraparam = parsed_values[3] if len(parsed_values) > 3 else None
        return key, low_value, high_value, step, extraparam
    else:
        return None
    
def load_hyperparameters_constraints_from_file(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            parsed = parse_hyperconstraints_line(line)
            if parsed:
                key, low_value, high_value, step, extraparam = parsed
                data_dict[key] = (low_value, high_value, step, extraparam)
    return data_dict



def pet_save(pet, filename):
    pickle.dump(pet, open(filename, "wb"))
# #guardamos en un binario
# def compressed_pickle(data):
#     with bz2.BZ2File(f"/content/drive/MyDrive/grupo1-saturdaysAI/data/save_dict3" + '.pbz2', 'w') as f:
#                cPickle.dump(data, f)

# Auxiliares para pickle

def pet_load(file):
    # pickle.load(open(f"/content/drive/MyDrive/grupo1-saturdaysAI/data/image_data.p", "rb"))
    return pickle.load(open(file, "rb"))


def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

class Logger:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.verbosity = 1
    def log(self, message, level):
        if self.verbosity  >= level:
            print(message)
            if self.file_path is not None:
                with open(self.file_path, 'a') as file:
                    file.write(f"{level}: {message}\n")