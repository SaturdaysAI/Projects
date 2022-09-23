import torch
import numpy as np

def denormalize_image(image:torch.Tensor) -> np.array:
    """
    Denormalize an image.
    Args:
        image (torch.Tensor): Image to denormalize.
    Returns:
        torch.Tensor: Denormalized image.
    """
    image = image.permute(1, 2, 0)
    image = image.numpy()
    image = image * 255.0
    image = image.astype(np.uint8)
    return image
