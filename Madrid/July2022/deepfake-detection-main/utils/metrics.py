"""
Metrics for binary image classification in PyTorch.
"""
import torch

def get_accuracy(output_labels, y_true, sigmoid=True):
    """Get the accuracy of a binary classification."""
    # Check that the dimensions are as expected
    assert y_true.ndim == 1 and y_true.size() == output_labels.size()

    if sigmoid:
        output_labels = torch.sigmoid(output_labels)

    output_labels = output_labels > 0.5

    return (y_true == output_labels).sum().item() / y_true.size(0)

if __name__ == "__main__":
    # Test get_accuracy function
    print("Test 1:")
    output_labels = torch.tensor([0.3, 0.2, 0.8, 0.9])
    y_true = torch.tensor([1, 0, 0, 0])
    acc = get_accuracy(output_labels, y_true, sigmoid=False)
    assert acc == 0.25, f"Accuracy should be 0.25, but it's {acc}"
    print("Test 1 passed")

    print("Test 2:")
    output_labels = torch.tensor([0.9, 0.8, 0.1, 0.9])
    y_true = torch.tensor([1, 1, 0, 0])
    acc = get_accuracy(output_labels, y_true, sigmoid=False)
    assert acc == 0.75, f"Accuracy should be 0.75, but it's {acc}"
    print("Test 2 passed")

    print("All tests passed successfully 🎉")
