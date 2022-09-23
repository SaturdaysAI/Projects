import os
import sys
import re

import pandas


class KOIFeatureExtractor:
    COLUMN_ID = 0
    COLUMN_NAME = 1
    COLUMN_LABEL = 3
    COLUMN_PERIOD = 10
    COLUMN_T0 = 13
    COLUMN_DURATION = 19

    def __init__(self, sourceFileName):
        self.sourceFileName = sourceFileName

    def extractTrainData(self, destinationFileName, mission):
        trainFileName = destinationFileName + "_train.csv"
        unlabeledFileName = destinationFileName + "_test.csv"

        print(f"Extracting features in dataset {self.sourceFileName} to files {trainFileName} and {unlabeledFileName}")
        # Delete destination files to be able to recreate it
        self.deleteFile(trainFileName)
        self.deleteFile(unlabeledFileName)
        sourceFile = pandas.read_csv(self.sourceFileName, sep=',')
        with open(trainFileName, 'a+') as trainFile, open(unlabeledFileName, 'a+') as unlabeledFile:
            # Header row for generated file
            trainFile.write("mission,koi_id,koi_name,koi_time0bk,koi_period,koi_duration,koi_is_planet\n")
            unlabeledFile.write("mission,koi_id,koi_name,koi_time0bk,koi_period,koi_duration\n")
            # Read each line in dataset
            if mission == 'TESS':
                for line in sourceFile.iterrows():
                    koiId = line[1].tid
                    koiName = line[1].toi
                    koiLabel = line[1].tfopwg_disp
                    koiPeriod = float(line[1].pl_orbper)
                    koiT0 = float(line[1].pl_tranmid)
                    koiDuration = float(line[1].pl_trandurh) / 24
                    LABEL_TRUE = 'CP'
                    LABEL_TRUE_2 = 'KP'
                    LABEL_FALSE = 'FA'
                    LABEL_FALSE_2 = 'FP'
                    TRAIN_LABELS = [LABEL_TRUE, LABEL_FALSE, LABEL_FALSE_2, LABEL_TRUE_2]
                    LABEL_CANDIDATE = 'PC'
                    LABEL_CANDIDATE_2 = 'APC'
                    LABEL_CANDIDATES = [LABEL_CANDIDATE, LABEL_CANDIDATE_2]
                    if koiLabel in TRAIN_LABELS:
                        trainFile.write('%s,%s,%s,%f,%f,%f,%d\n' % (
                        mission, koiId, koiName, koiT0, koiPeriod, koiDuration,
                        self.toDummy(koiLabel, LABEL_TRUE, LABEL_FALSE, LABEL_TRUE_2, LABEL_FALSE_2)))
                    if koiLabel in LABEL_CANDIDATES:
                        unlabeledFile.write(
                            '%s,%s,%s,%f,%f,%f\n' % (mission, koiId, koiName, koiT0, koiPeriod, koiDuration))
            else:
                for line in sourceFile.iterrows():
                    koiId = line[1].kepid
                    koiName = line[1].kepoi_name
                    koiLabel = line[1].koi_disposition
                    koiPeriod = float(line[1].koi_period)
                    koiT0 = float(line[1].koi_time0bk)
                    koiDuration = float(line[1].koi_duration) / 24
                    LABEL_TRUE = 'CONFIRMED'
                    LABEL_FALSE = 'FALSE POSITIVE'
                    TRAIN_LABELS = [LABEL_TRUE, LABEL_FALSE]
                    LABEL_CANDIDATE = 'CANDIDATE'
                    # We are only interested in KOIs with CONFIRMED of FALSE POSITIVE TCEs
                    if koiLabel in TRAIN_LABELS:
                        trainFile.write('Kepler,%s,%s,%f,%f,%f,%d\n' % (
                        koiId, koiName, koiT0, koiPeriod, koiDuration, self.toDummy(koiLabel, LABEL_TRUE, LABEL_FALSE)))
                    if koiLabel == LABEL_CANDIDATE:
                        unlabeledFile.write('Kepler,%s,%s,%f,%f,%f\n' % (koiId, koiName, koiT0, koiPeriod, koiDuration))

    def toDummy(self, label, LABEL_TRUE, LABEL_FALSE, LABEL_TRUE_2=None, LABEL_FALSE_2=None):
        if label == LABEL_TRUE:
            return 1
        if label == LABEL_FALSE:
            return 0
        if LABEL_TRUE_2 and LABEL_FALSE_2:
            if label == LABEL_TRUE_2:
                return 1
            if label == LABEL_FALSE_2:
                return 0
        print("Error: label ", label, "not recognized")
        return -1

    def deleteFile(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)


# Execute only if script run standalone (not imported)
if __name__ == '__main__':
    (script, sourceFileName, trainFileName, mission) = sys.argv
    extractor = KOIFeatureExtractor(sourceFileName)
    extractor.extractTrainData(trainFileName, mission)