import os
import torch
import torch.utils.data as data_utils
from torch import nn
from torch import optim
from facenet_pytorch import InceptionResnetV1
from tqdm import tqdm
from random import randint
import matplotlib.pyplot as plt
import wandb
from utils.denormalize_image import denormalize_image
from utils.metrics import get_accuracy
from utils.dict_to_struct import DictStructure
from dataset.faces import Faces

FACES_FOLDER = os.path.join("data", "faces")
FACES_CSV = os.path.join(FACES_FOLDER, "faces.csv")
VALIDATION_SPLIT = 0.2
CLASS_NAMES = {0: "real", 1: "fake"}


def make(config):
    """Create the dataloaders, the model, the criterion & the optimizer"""
    if isinstance(config, wandb.Config):
        print("Using the configuration from wandb.config")
    elif isinstance(config, dict):
        print("Not using the configuration from wandb.config")
        config = DictStructure(config)
    else:
        raise ValueError("config must be a wandb.Config or a dict")

    # Make the data
    train_dataset = get_data(split="training", transform=True, print_ds_len=True)
    val_dataset = get_data(split="validation", transform=True, print_ds_len=False)
    train_loader = make_loader(train_dataset, batch_size=config.batch_size)
    val_loader = make_loader(val_dataset, batch_size=config.batch_size)

    # Make the model
    model = InceptionResnetV1(
        pretrained=config.pretrained_dataset,
        classify=True,
        num_classes=config.classes,
        device=DEVICE,
    )

    # Make the loss and optimizer
    criterion = nn.BCEWithLogitsLoss()  # sigmoid + binary cross entropy
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

    return model, train_loader, val_loader, criterion, optimizer


def get_data(
    split: str = "training", transform: bool = True, print_ds_len: bool = None
):
    """Get the dataset.
    
    Args:
        split (str): Split of the dataset to use: 'training' or 'validation'
        transform (bool, optional): Perform transformations on the data or not
        print_ds_len (bool, optional): Print the length of the original dataset
    """
    # Check that the arguments are as expected
    assert split in [
        "training",
        "validation",
    ], "Split must be 'training' or 'validation'"
    assert transform in [True, False], "Transform must be True or False"

    # Create the dataset
    full_dataset = Faces(
        root=FACES_FOLDER, csv=FACES_CSV, split=split, transform=transform
    )
    if print_ds_len:
        print(f"Original dataset length: {len(full_dataset)}")

    # Set where the subsets should start and end
    end_idx = (
        round((1 - VALIDATION_SPLIT) * len(full_dataset))
        if split == "training"
        else len(full_dataset)
    )
    begin_idx = (
        0 if split == "training" else round((1 - VALIDATION_SPLIT) * len(full_dataset))
    )

    # Create the subsets
    subset_indices = torch.arange(begin_idx, end_idx)
    subset_dataset = data_utils.Subset(full_dataset, subset_indices)

    print(
        f"{split} dataset length ({round(len(subset_dataset) / len(full_dataset), 2)*100}%): {len(subset_dataset)}"
    )

    return subset_dataset


def make_loader(dataset, batch_size):
    """Create the Data Loader for the dataset."""
    loader = data_utils.DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        pin_memory=True,
        num_workers=2,
    )
    return loader


def train_batch(images, labels, model, criterion, split="training", optimizer=None):
    """Train a batch of data."""
    if split == "training":
        assert optimizer is not None, "Optimizer must be provided for training"
    assert split in [
        "training",
        "validation",
    ], "Split must be 'training' or 'validation'"

    images = images.to(device=DEVICE)
    labels = labels.to(device=DEVICE)

    # Forward pass
    outputs = model(images).squeeze()

    loss = criterion(outputs, labels)
    acc = get_accuracy(outputs, labels)

    if split == "training":
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return loss.item(), acc


def model_pipeline(hyperparameters):
    # tell wandb to get started
    with wandb.init(project="deepfake-detection", config=hyperparameters):
        # access all HPs through wandb.config, so logging matches execution!
        config = wandb.config

        # make the model, data, and optimization problem
        model, train_loader, val_loader, criterion, optimizer = make(config)

        # and use them to train the model
        train(model, train_loader, val_loader, criterion, optimizer, config)

    return model


def save_model(model, optimizer, loss, base_path, epoch):
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "validation_loss": loss,
        },
        f"{base_path}_epoch_{epoch}.pth",
    )


def train(model, train_loader, val_loader, criterion, optimizer, config):
    """Train the model and save the information on Weights and Biases."""
    print("Beginning training 🎨")
    wandb.watch(model, criterion, log="all", log_freq=10)

    history = {"loss": {"train": [], "val": []}, "acc": {"train": [], "val": []}}
    batches_seen = 0
    base_path = "./models/resnetinceptionv1"

    for epoch in range(config.epochs):
        # Training
        acc_per_epoch_train, loss_per_epoch_train = 0, 0
        model.train()
        for _, (images_batch, labels_batch) in enumerate(tqdm(train_loader)):
            loss, acc = train_batch(
                images_batch, labels_batch, model, criterion, "training", optimizer
            )

            batches_seen += 1
            acc_per_epoch_train += acc
            loss_per_epoch_train += loss

        # Validation
        with torch.no_grad():
            acc_per_epoch_val, loss_per_epoch_val = 0, 0
            model.eval()
            for _, (images_batch, labels_batch) in enumerate(tqdm(val_loader)):
                loss, acc = train_batch(
                    images_batch, labels_batch, model, criterion, "validation"
                )

                acc_per_epoch_val += acc
                loss_per_epoch_val += loss

        history["loss"]["train"].append(loss_per_epoch_train / len(train_loader))
        history["loss"]["val"].append(loss_per_epoch_val / len(val_loader))
        history["acc"]["train"].append(acc_per_epoch_train / len(train_loader))
        history["acc"]["val"].append(acc_per_epoch_val / len(val_loader))

        print(f"Epoch [{epoch + 1}/{config.epochs}]")
        print(
            f"\tTrain Loss: {history['loss']['train'][epoch]:.4f}, Train Acc: {history['acc']['train'][epoch]*100:.2f}%"
        )
        print(
            f"\tVal Loss: {history['loss']['val'][epoch]:.4f}, Val Acc: {history['acc']['val'][epoch]*100:.2f}%",
            end="\n\n",
        )

        wandb.log(
            {
                "Epoch": epoch + 1,
                "Train Loss": history["loss"]["train"][epoch],
                "Val Loss": history["loss"]["val"][epoch],
                "Train Acc": round(history["acc"]["train"][epoch] * 100, 2),
                "Val Acc": round(history["acc"]["val"][epoch] * 100, 2),
            },
            step=batches_seen,
        )

        if (epoch + 1) % config.save_every == 0:
            save_model(
                model, optimizer, history["loss"]["val"][epoch], base_path, epoch + 1
            )


if __name__ == "__main__":
    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Running on device: {DEVICE.upper()}")

    config = dict(
        epochs=10,
        save_every=2,  # save the model every 2 epochs
        classes=1,  # binary classification
        batch_size=16,
        learning_rate=0.001,
        dataset="FaceForensics++",
        architecture="InceptionResNetV1",
        pretrained_dataset="vggface2"
    )

    model = model_pipeline(config)
    torch.save(model.state_dict(), "./models/resnetinceptionv1_final.pth")
