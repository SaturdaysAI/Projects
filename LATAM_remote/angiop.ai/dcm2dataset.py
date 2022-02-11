import os
import torch
import pydicom
import numpy as np
import torchvision.transforms as transforms
from torch.utils.data import Dataset

"""
# Train images: ImageData/train/0; ImageData/train/1
# Test images: ImageData/test/0; ImageData/test/1
# Classes: "not_operable": 0; "operable":1
#
# set_file_matrix():
# Count total items in sub-folders of root/image_dir:
# Create a list with all items from root/image_dir "(pixel_array, label)"
# Takes label from sub-folder name "0" or "1"
"""


class DicomDataset(Dataset):
    def __init__(self, root, image_dir):
        self.image_dir = os.path.join(root, image_dir)  # ImageData/train or ImageData/test
        #self.image_dir = image_dir
        self.data = self.set_file_matrix()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(256)
            #transforms.RandomHorizontalFlip()
        ])

    def __len__(self):
        return len(self.data)

    def set_file_matrix(self):
        # count elements
        total = 0
        root = self.image_dir
        folders = ([name for name in os.listdir(root)
                    if os.path.isdir(os.path.join(root, name))])
        for folder in folders:
            new_path = os.path.join(root, folder)
            contents = len([name for name in os.listdir(new_path) if os.path.isfile(os.path.join(new_path, name))])
            total += contents

        # create list(img_name, label)
        files = []
        labels = ([name for name in os.listdir(root)
                   if os.path.isdir(os.path.join(root, name))])
        for label in labels:
            new_path = os.path.join(root, label)
            file_list = os.listdir(new_path)
            for file in file_list:
                files.append([file, label])

        return files

    def __getitem__(self, index):
        try:
            image_file = pydicom.dcmread(os.path.join(self.image_dir, self.data[index][1], self.data[index][0]), force=True)
            image = np.array(image_file.pixel_array, dtype=np.float32)[np.newaxis]  # Add channel dimension
            image = (image - np.min(image)) / np.ptp(image)

            image = torch.from_numpy(image)
            label = float(self.data[index][1])
            if self.transform:
                image = self.transform(image)

            return image, label
        except Exception as ex:
            return None, None
