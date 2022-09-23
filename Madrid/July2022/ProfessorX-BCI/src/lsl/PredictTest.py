import pickle
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy.signal import butter, lfilter, lfilter_zi
import pandas as pd
import requests


## UTILS

def getStrTime():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S.%f")
    return date_time


def getStrTime2():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d_%m_%Y__%H_%M_%S")
    return date_time


def loadModel(filename):
    path_file = Path("..", "..", "models", filename)
    file = open(path_file, 'rb')
    loaded_model = pickle.load(file)
    print("--- loading model --->", loaded_model)
    file.close()
    return loaded_model


def loadArtifact(filename):
    path_file = Path("..", "..", "data", "pickle", filename)
    file = open(path_file, 'rb')
    loaded_artifact = pickle.load(file)
    #print("--- loading artifact, nsamples --->", len(loaded_artifact))
    file.close()
    return loaded_artifact


def generateDfWindowChannel(window, n_samples):
    map_to_df = {}
    for n_sample in range(n_samples):
        sample = window[n_sample]
        map_to_df[n_sample] = [sample]
    return pd.DataFrame(map_to_df)


## FILTERING CLASSES

class BandPass:
    def __init__(self, lowcut, highcut, sr, order=4):
        self.b, self.a = butter(order, [lowcut, highcut], btype='bandpass', fs=sr)
        self.z = lfilter_zi(self.b, self.a)

    def filter(self, x):
        y, self.z = lfilter(self.b, self.a, x, zi=self.z)
        return y


class BandStop:
    def __init__(self, lowcut, highcut, sr, order=4):
        self.b, self.a = butter(order, [lowcut, highcut], btype='bandstop', fs=sr)
        self.z = lfilter_zi(self.b, self.a)

    def filter(self, x):
        y, self.z = lfilter(self.b, self.a, x, zi=self.z)
        return y


class EEGClassifier:

    def __init__(self):
        self.duration = 2.5
        self.n_samples_window = int(256 * self.duration)  # IMPORTANT!! depends on classifier input

        self.actions_map = {
            0: 'no action',  # basal
            1: 'left',  # jaw
            2: 'right'  # left blink
        }
        self.model = loadModel('channel3_two_and_a_half_seconds_windows_rubert_jaw_and_left_blink_regression.pkl')
        self.load_artifacts()
        self.prepareFilter()

    def load_artifacts(self):
        self.artifacts_test = []
        basal_test = loadArtifact('channel_3_rubert_basal.pkl')
        jaw_test = loadArtifact('channel_3_rubert_jaw.pkl')
        blink_test = loadArtifact('channel_3_rubert_left_blink.pkl')
        self.artifacts_test.append(basal_test)
        self.artifacts_test.append(jaw_test)
        self.artifacts_test.append(blink_test)

    def prepareFilter(self):
        self.sr = 246
        n = int(self.sr * self.duration)
        lowcut = 0.5
        highcut = 100
        order = 4
        channel_count = 16
        self.filter_bandpass = BandPass(lowcut, highcut, self.sr, order)
        self.notch = BandStop(48, 52, self.sr, order)
        self.t = np.linspace(0, self.duration, n, endpoint=False)

    def classify_signal_into_action(self, window_channel):
        df = generateDfWindowChannel(window_channel, len(window_channel))
        predicted = self.model.predict(df)
        print("--- predicted --->", predicted[0])
        return predicted

    def launch_drone_action(self, action):
        print("--- action --->", action)
        url = 'http://localhost:5000/drone/' + action
        res = requests.get(url)
        print("--- response --->", res.text)


if __name__ == '__main__':
    classifier_offline = EEGClassifier()

    basal = classifier_offline.artifacts_test[0]
    jaw = classifier_offline.artifacts_test[1]
    blink = classifier_offline.artifacts_test[2]

    artifact_test = blink
    filtered_artifact = classifier_offline.filter_bandpass.filter(classifier_offline.notch
                                                                  .filter(artifact_test))

    predicted = classifier_offline.classify_signal_into_action(filtered_artifact)
    action = classifier_offline.actions_map[int(predicted)]
    print('action --> ', action)
    classifier_offline.launch_drone_action(action)
    print('action --> ', "land")
    classifier_offline.launch_drone_action("land")
