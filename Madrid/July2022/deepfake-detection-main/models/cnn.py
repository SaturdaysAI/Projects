# Imports
import torch
import torchvision # torch package for vision related things
import torch.nn.functional as F  # Parameterless functions, like (some) activation functions
import torchvision.datasets as datasets  # Standard datasets
import torchvision.transforms as transforms  # Transformations we can perform on our dataset for augmentation
from torch import optim  # For optimizers like SGD, Adam, etc.
from torch import nn  # All neural network modules
from torch.utils.data import DataLoader  # Gives easier dataset managment by creating mini batches etc.
from tqdm import tqdm  # For nice progress bar!
import cv2
import os
from torchvision.io import read_image
import pandas as pd
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import numpy as np




DATA_FOLDER = os.path.join("..", "data")
ORIGINAL_VIDEOS_FOLDER = os.path.join(
    DATA_FOLDER, "original_sequences", "actors", "c40", "videos"
)
FAKE_VIDEOS_FOLDER = os.path.join(
    DATA_FOLDER, "manipulated_sequences", "DeepFakeDetection", "c40", "videos"
)
FACES_FOLDER = os.path.join(DATA_FOLDER, "faces")
FACES_REAL = os.path.join(FACES_FOLDER, "real")
FACES_FAKE = os.path.join(FACES_FOLDER, "fake")
CARAS = os.path.join(FACES_FOLDER, "caras")
FACES_CSV = os.path.join(FACES_FOLDER, "faces2.csv")







# Simple CNN
class CNN(nn.Module):
    def __init__(self, in_channels=3, num_classes=2):
        super(CNN, self).__init__() 
        self.conv1 = nn.Conv2d(
            in_channels=in_channels,
            out_channels=8,
            kernel_size=(3, 3), stride=(1, 1),
            padding=(1, 1),
        )
        
        self.pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.conv2 = nn.Conv2d(
            in_channels=8,
            out_channels=16,
            kernel_size=(3, 3),
            stride=(1, 1),
            padding=(1, 1),
        )
     
        self.fc1 = nn.Linear(16 * 64 * 64, num_classes)#256x256
 
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc1(x)
        return x

  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")




class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transforms = None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transforms = transforms

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):

        if  self.img_labels.iloc[idx, 2] == 'real':
            img_path = os.path.join(self.img_dir, 'real',  str(self.img_labels.iloc[idx, 1]))
        else:
            img_path = os.path.join(self.img_dir, 'fake', str(self.img_labels.iloc[idx, 1]))

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0
        image = image.astype(np.float32)

        if self.transforms:
            image = self.transforms(image)

        label = self.img_labels.iloc[idx, 2]

        return image, label


data = CustomImageDataset(FACES_CSV, FACES_FOLDER, transforms.ToTensor())
print(data[6])

in_channels = 3
num_classes = 2
learning_rate = 0.001
batch_size = 64
num_epochs = 1


dataset = CustomImageDataset(FACES_CSV, FACES_FOLDER, transforms.ToTensor())

train_set, test_set = torch.utils.data.random_split(dataset, [3000, 215])
train_loader = DataLoader(dataset=train_set, batch_size= batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size= batch_size, shuffle=True)



# Initialize network
model = CNN(in_channels=in_channels, num_classes=num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train Network
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(tqdm(train_loader)):

        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        # backward
        optimizer.zero_grad()
        loss.backward()

        # gradient descent or adam step
        optimizer.step()
#aqui no tenemos que cambiar el tamaño porque es algo que ya hemos hecho en la preparacion de la red

