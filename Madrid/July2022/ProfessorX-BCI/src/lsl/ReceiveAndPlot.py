import os
import pickle
from pathlib import Path
from datetime import datetime
import numpy as np
from pylsl import StreamInlet, resolve_stream
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
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


def saveWindowPickle(window):
    path_file = Path("..", "..", "data", "pickle", "window_" + getStrTime2() + ".pickle")
    file = open(path_file, "wb")
    pickle.dump(window, file)
    file.close()


def loadModel(filename):
    path_file = Path("..", "..", "models", filename)
    file = open(path_file, 'rb')
    loaded_model = pickle.load(file)
    print("--- loading model --->", loaded_model)
    file.close()
    return loaded_model


def generateDfWindowChannel(window, pos_array_channel, nsamples):
    map_to_df = {}
    for n_sample in range(nsamples):
        sample = window[n_sample][pos_array_channel]
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


## PLOTING

class CustomViewBox(pg.ViewBox):
    def __init__(self, viewer, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.viewer = viewer

    def wheelEvent(self, ev, axis=None):
        self.viewer.scale *= 1.25 if ev.delta() < 0 else 1 / 1.25


## MAIN CLASS

class EEGViewer:
    def __init__(self):
        self.plot_duration = 2.5
        self.scale = 160
        self.n_samples_window = int(256 * self.plot_duration)  # IMPORTANT!! depends on classifier input

        self.windows_queue = []
        self.window_buffer = {'timestamp': '', 'data': []}
        self.samplesCounter = 0
        self.model = loadModel('channel3_two_and_a_half_seconds_windows_rubert_jaw_and_left_blink_regression.pkl')
        self.actions_map = {
            0: 'no action',  # basal
            1: 'fire',  # jaw
            2: 'moveLeft'  # left blink
        }

    def connect(self):
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')
        self.inlet = StreamInlet(streams[0])
        self.prepareFilter()
        self.preparePlot()
        self.start()

    def prepareFilter(self):
        self.sr = self.inlet.info().nominal_srate()
        n = int(self.sr * self.plot_duration)
        lowcut = 0.5
        highcut = 30
        order = 4
        self.filter = [BandPass(lowcut, highcut, self.sr, order) for i in range(self.inlet.channel_count)]
        self.notch = [BandStop(48, 52, self.sr, order) for i in range(self.inlet.channel_count)]
        self.buffer = np.zeros((self.inlet.channel_count, n))
        self.t = np.linspace(0, self.plot_duration, n, endpoint=False)

    def preparePlot(self):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('LSL Plot ' + self.inlet.info().name())
        self.vb = CustomViewBox(self)
        self.plt = self.win.addPlot(viewBox=self.vb)
        self.plt.setXRange(0, self.plot_duration)
        self.plt.setYRange(-1 - self.inlet.channel_count, 1)
        self.plt.setMouseEnabled(False, False)
        self.plt.hideAxis('left')
        self.plt.hideButtons()
        self.plt.setMenuEnabled(False)
        self.plt.setTitle(self.inlet.info().name())
        self.curves = [self.plt.plot() for x in range(self.inlet.channel_count)]

    def prepareLog(self):
        log_path_file = Path("..", "..", "log", "lsl_record_" + getStrTime2() + ".log")
        self.logfile = open(log_path_file, "a")
        self.logfile.write(self.inlet.info().name() + "\n")

    def writeLog(self, channels_sample):
        self.logfile.write(getStrTime() + "\n")
        self.logfile.write(str(len(channels_sample)) + "\n")
        # self.logfile.write(np.array_str(channels_sample) + "\n")

    def saveTemporalWindows(self, channels_sample):
        self.window_buffer['data'].append(channels_sample)
        self.samplesCounter = self.samplesCounter + 1

        if self.samplesCounter == self.n_samples_window:
            self.window_buffer['timestamp'] = getStrTime()
            win_copy = self.window_buffer.copy()
            self.windows_queue.append(win_copy)
            # saveWindowPickle(self.window_buffer)

            predicted = self.classify_signal_into_action(win_copy['data'])
            action = self.actions_map[int(predicted)]
            print('action --> ', action)
            # self.launchDroneAction(action)

            ## reset window buffer
            self.window_buffer['data'] = []
            self.samplesCounter = 0

    def classify_signal_into_action(self, window):
        channel_selected = 3
        df = generateDfWindowChannel(window, channel_selected - 1, self.n_samples_window)
        predicted = self.model.predict(df)
        print("--- predicted --->", predicted[0])
        return predicted

    def launch_drone_action(self, action):
        print("--- action --->", action)
        url = 'http://localhost:5000/drone/' + action
        res = requests.get(url)
        print("--- response --->", res.text)

    def start(self):
        self.prepareLog()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def update(self):
        # Read data from the inlet. Use a timeout of 0.0 so we don't block GUI interaction.
        chunk, timestamps = self.inlet.pull_chunk()
        # chunk, timestamps len --> 8, 11, 24, 32, 40, 78...
        # timestamps[0] --> 1567.4086744
        if timestamps:
            y = np.asarray(chunk)
            samples = y.shape[0]
            # samples --> 8 16 24 32...
            self.buffer = np.roll(self.buffer, -samples, axis=1)
            # buffer shape --> (16, 256 * duration)

            for ch_ix in range(self.inlet.channel_count):
                filtered_y = self.filter[ch_ix].filter(self.notch[ch_ix].filter(y[:, ch_ix]))
                self.buffer[ch_ix, -samples:] = filtered_y  # filling channels sample buffer --> every 1/256 seg, sample rate
                # channel_samples = self.buffer[ch_ix]  # len --> 256 * duration
                self.curves[ch_ix].setData(self.t, self.buffer[ch_ix, :] / self.scale - ch_ix)

            ### Buffer channels samples READY --> every 5ms, too late to generate windows

            # self.writeLog(self.buffer)
            # try:
            #    self.saveTemporalWindows(self.buffer)
            # except Exception as e:
            #    print("---error---", e)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    viewer = EEGViewer()
    viewer.connect()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
