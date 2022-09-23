import numpy as np
import pandas as pd
from math import floor
import matplotlib.pyplot as plt

def filters(raw, fmin=0.5, fmax=100., notch=50., sampling_rate=250, fir_design='firwin'):
    '''Apply high/low-pass and notch filters:

        === Args ===
        * raw - mne Raw object: object to apply filters on
        * fmin, fmax - float: bandpass frequencies
        * notch - float: powerline (AC current) frequecy
        * ny_freq - float: Nyquist frequency. Half of the sampling rate
        * fir_design: str: Notch filter type. See mne doc for more details
        * sampling_rate - int, float: sampling rate of the measured data

        === Returns ===
        * raw_c - mne Raw object: Processed Raw copy
        '''
    raw_c = raw.copy()
    raw_c.filter_bandpass(l_freq=fmin, h_freq=fmax)
    raw_c.notch_filter(np.arange(notch, sampling_rate / 2, notch), fir_design=fir_design)
    return raw_c


def signal_df_to_windows(eeg_data, chunk_size=100, n_channels=16):
    n_chunks = floor(eeg_data.shape[0] / chunk_size)

    windows = np.ndarray(shape=(n_channels, n_chunks, chunk_size), dtype=float)

    channels_array = []
    for i in range(1, n_channels + 1):
        channels_array.append("EEG-ch" + str(i))
    channels_as_pd = eeg_data[channels_array].to_numpy()

    # shape --> (samplesChannel, nChannels)

    for iChannel in range(n_channels):
        for iChunk in range(n_chunks):
            for iSample in range(chunk_size):
                idf = (iChunk * chunk_size) + iSample
                windows[iChannel][iChunk][iSample] = channels_as_pd[idf][iChannel]

    # shape --> (channels, windows, samples)
    return windows

def signal_raw_to_windows(eeg_data, chunk_size=100, n_channels=16):
    n_chunks = floor(eeg_data.shape[1] / chunk_size)

    windows = np.ndarray(shape=(n_channels, n_chunks, chunk_size), dtype=float)

    # shape --> (nChannels, samplesChannel)

    for iChannel in range(n_channels):
        for iChunk in range(n_chunks):
            for iSample in range(chunk_size):
                idf = (iChunk * chunk_size) + iSample
                windows[iChannel][iChunk][iSample] = eeg_data[iChannel][idf]

    # shape --> (channels, windows, samples)
    return windows

def channels_to_list_df(channels_data, artifact_label):
    # shape --> (channels, windows, samples)

    channels_list_df = []

    for channelData in channels_data:
        channel_data_map = {'label': []}

        for iWindow, window in enumerate(channelData):
            even = (iWindow % 2) == 0
            label = artifact_label if (even and iWindow != 0) else "pause"
            channel_data_map['label'].append(label)

            for iSample, sample in enumerate(window):
                if iSample in channel_data_map:
                    channel_data_map[iSample].append(sample)
                else:
                    channel_data_map[iSample] = [sample]

        channel_data_df = pd.DataFrame(channel_data_map)
        channels_list_df.append(channel_data_df)
        # df.columns = ['window', 'label']

    # array --> df(window, sample) + last column label
    return channels_list_df

def channels_to_list_df2(channels_data, artifact_label):
    # shape --> (channels, windows, samples)

    channels_list_df = []

    for channelData in channels_data:
        channel_data_map = {'label': []}

        for iWindow, window in enumerate(channelData):
            multiple_of_four = (iWindow % 4) == 0
            label = artifact_label if (multiple_of_four and iWindow != 0) else "pause"
            channel_data_map['label'].append(label)

            for iSample, sample in enumerate(window):
                if iSample in channel_data_map:
                    channel_data_map[iSample].append(sample)
                else:
                    channel_data_map[iSample] = [sample]

        channel_data_df = pd.DataFrame(channel_data_map)
        channels_list_df.append(channel_data_df)
        # df.columns = ['window', 'label']

    # array --> df(window, sample) + last column label
    return channels_list_df

# Funcion para visualizar las ventanas a ver si caen correctamente en un spike:
def print_windows(allChannelsData):
  for idChannel, channel in enumerate(allChannelsData):
    for idWindow, window in enumerate(channel):
      plt.figure(figsize=(4,4))
      plt.title(f"window {idWindow} from channel {idChannel}")
      plt.plot(window)