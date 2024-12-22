import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision.models import ConvNeXt_Tiny_Weights

class Network(nn.Module):
    def __init__(self, num_classes=29):
        super(Network, self).__init__()
        self.convnext = torchvision.models.convnext_tiny(weights=ConvNeXt_Tiny_Weights.IMAGENET1K_V1)
        
        # Modify the first conv layer to accept 1 channel instead of 3 (for grayscale images)
        conv1 = self.convnext.features[0][0]
        self.convnext.features[0][0] = nn.Conv2d(
            in_channels=1,  # Grayscale images have 1 channel
            out_channels=conv1.out_channels,
            kernel_size=conv1.kernel_size,
            stride=conv1.stride,
            padding=conv1.padding,
            bias=True if conv1.bias is not None else False  # Properly handle the bias argument
        )
        
        # Modify the final fully connected layer to match the number of classes
        in_features = self.convnext.classifier[2].in_features
        self.convnext.classifier[2] = nn.Linear(in_features, num_classes)
        
        # Add softmax for output (optional, depending on loss function)
        self.softmax = nn.LogSoftmax(dim=1)
        
    def forward(self,x):
        x = self.convnext(x)  # Forward pass through ConvNeXt
        x = self.softmax(x)   # Apply softmax for class probabilities
        return x