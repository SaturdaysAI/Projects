from mne_realtime import MockLSLStream, LSLClient
import bbtools as bbt
import matplotlib.pyplot as plt



# this is the host id that identifies your stream on LSL
host = 'localhost'
# this is the max wait time in seconds until client connection
wait_max = 5

# data
raw = bbt.read_csv(
    "../../data/Rubert_14_may/Rubert_mordida_1/EEG.csv",
    ['Fp1', 'Fp2', 'F3', 'F4', 'C1', 'C3', 'C2', 'C4', 'CP1', 'CP3', 'CP2', 'CP4', 'Cz', 'O1', 'O2', 'Pz']
)

def ploting():
    # Let's observe it
    plt.ion()  # make plot interactive
    _, ax = plt.subplots(1)
    with LSLClient(info=raw.info, host=host, wait_max=wait_max) as client:
        client_info = client.get_measurement_info()
        sfreq = int(client_info['sfreq'])
        print(client_info)

        # let's observe ten seconds of data
        for ii in range(10):
            plt.cla()
            epoch = client.get_data_as_epoch(n_samples=sfreq)
            epoch.average().plot(axes=ax)
            plt.pause(1)
    plt.draw()

def logging():
    with LSLClient(info=raw.info, host=host, wait_max=wait_max) as client:
        client_info = client.get_measurement_info()
        sfreq = int(client_info['sfreq'])
        print(client_info)

        # let's observe ten seconds of data
        for ii in range(10):
            epoch = client.get_data_as_epoch(n_samples=sfreq)
            average = epoch.average()
            print(average)

def startMockServer():
    # For this example, let's use the mock LSL stream.
    stream = MockLSLStream(host, raw, 'eeg', time_dilation=2)
    stream.start()

if __name__ == '__main__':
    startMockServer()
    #ploting()
    logging()