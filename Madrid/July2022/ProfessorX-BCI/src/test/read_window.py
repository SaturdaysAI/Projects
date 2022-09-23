import pickle
from pathlib import Path

def printPickle(file_name):
    path_file = Path("..", "..", "data", "pickle", file_name)

    print('---File---')
    print(path_file)

    with open(path_file, 'rb') as pickle_file:
        loaded_window = pickle.load(pickle_file)
        pickle_file.close()

    print("--init--")
    print(loaded_window['timestamp_init'])

    print("--end--")
    print(loaded_window['timestamp_init'])

    print("--first sample--")
    print(loaded_window['data'][240])

if __name__ == '__main__':
    printPickle("window_26_05_2022__20_29_26.pickle")