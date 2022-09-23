"""
Constants that we'll be used for the dataset.

Copyright (c), Aarón, Jaime, Nacho & Conchi - All Rights Reserved

This source code is licensed under the Apache license found in the
LICENSE file in the root directory of this source tree:
https://github.com/aaronespasa/deepfake-detection/blob/main/LICENSE
"""
import os

DATA_FOLDER = os.path.join("..", "data")
ORIGINAL_VIDEOS_FOLDER = os.path.join(
    DATA_FOLDER, "original_sequences", "actors", "c23", "videos"
)
FAKE_VIDEOS_FOLDER = os.path.join(
    DATA_FOLDER, "manipulated_sequences", "DeepFakeDetection", "c23", "videos"
)
FACES_FOLDER = os.path.join(DATA_FOLDER, "faces")
FACES_REAL = os.path.join(FACES_FOLDER, "real")
FACES_FAKE = os.path.join(FACES_FOLDER, "fake")
FACES_CSV = os.path.join(FACES_FOLDER, "faces.csv")
