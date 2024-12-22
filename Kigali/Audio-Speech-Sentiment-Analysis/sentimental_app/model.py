import torch
import torch.nn as nn

class SentimentModel(nn.Module):
    def __init__(self):
        super(SentimentModel, self).__init__()
        
        # Convolutional layer with exact dimensions from saved model
        self.conv1 = nn.Conv1d(in_channels=64, out_channels=32, kernel_size=3)
        self.bn1 = nn.BatchNorm1d(32)
        
        # Fully connected layers with exact dimensions from saved model
        self.fc1 = nn.Linear(3029, 2048)
        self.fc2 = nn.Linear(2048, 1024)
        self.fc3 = nn.Linear(1024, 3200)
        self.fc4 = nn.Linear(1536, 256)  # Note the dimension change
        self.fc5 = nn.Linear(256, 64)
        self.output = nn.Linear(64, 3)
        
        # Activation and regularization
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        
    def forward(self, x):
        # Ensure input is correctly shaped
        if len(x.shape) == 1:
            x = x.unsqueeze(0)  # Add batch dimension
            
        # Reshape for conv1d - expecting (batch_size, 64, sequence_length)
        x = x.reshape(x.size(0), 64, -1)
        
        # Convolutional layer
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        
        # Flatten and reshape for first fc layer
        x = x.reshape(x.size(0), -1)
        # Pad or truncate to match fc1 input size
        if x.size(1) < 3029:
            x = torch.nn.functional.pad(x, (0, 3029 - x.size(1)))
        else:
            x = x[:, :3029]
        
        # Fully connected layers
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        
        x = self.relu(self.fc3(x))
        x = self.dropout(x)
        
        # Adjust dimension for fc4 input
        x = x[:, :1536]  # Take first 1536 features
        
        x = self.relu(self.fc4(x))
        x = self.dropout(x)
        
        x = self.relu(self.fc5(x))
        x = self.dropout(x)
        
        x = self.output(x)
        
        return x

# Example usage and testing
if __name__ == "__main__":
    # Create model instance
    model = SentimentModel()
    
    # Test with sample input
    sample_input = torch.randn(1, 2048)  # Single sample
    print(f"Input shape: {sample_input.shape}")
    
    try:
        output = model(sample_input)
        print(f"Output shape: {output.shape}")  # Should be [1, 3]
        
        # Print model structure with parameter shapes
        print("\nModel structure:")
        for name, param in model.named_parameters():
            print(f"{name}: {param.shape}")
            
    except Exception as e:
        print(f"Error during forward pass: {str(e)}")