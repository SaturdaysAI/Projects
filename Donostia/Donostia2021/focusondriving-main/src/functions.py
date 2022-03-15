import keras
import tensorflow as tf
import numpy as np
import sys
print(f'{sys.version}')
print(f'keras {keras.__version__}')
print(f'tensorflow {tf.__version__}')
print(f'numpy {np.__version__}')

import pandas as pd
import os
from imutils import paths
import cv2
import matplotlib.pyplot as plt
from PIL import Image

from keras.models import Model
from keras.optimizers import Adam
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Dropout, Flatten
from pathlib import Path
from livelossplot.inputs.keras import PlotLossesCallback
from sklearn.metrics import accuracy_score

import seaborn as sns
from sklearn.metrics import confusion_matrix


def create_model(input_shape, n_classes, optimizer='rmsprop', fine_tune=0, n_model=1):

    """
    Compiles a model integrated with VGG16 pretrained layers
    
    input_shape: tuple - the shape of input images (width, height, channels)
    n_classes: int - number of classes for the output layer
    optimizer: string - instantiated optimizer to use for training. Defaults to 'RMSProp'
    fine_tune: int - The number of pre-trained layers to unfreeze.
                If set to 0, all pretrained layers will freeze during training
    """
    # Pretrained convolutional layers are loaded using the Imagenet weights.
    # Include_top is set to False, in order to exclude the model's fully-connected layers.
    if n_model == 4:
        conv_base = VGG19(include_top=False,
                     weights='imagenet', 
                     input_shape=input_shape)
    else:
        conv_base = VGG16(include_top=False,
                         weights='imagenet', 
                         input_shape=input_shape)
    
    # Defines how many layers to freeze during training.
    # Layers in the convolutional base are switched from trainable to non-trainable
    # depending on the size of the fine-tuning parameter.
    if fine_tune > 0:
        for layer in conv_base.layers[:-fine_tune]:
            layer.trainable = False
    else:
        for layer in conv_base.layers:
            layer.trainable = False

    # Create a new 'top' of the model (i.e. fully-connected layers).
    # This is 'bootstrapping' a new top_model onto the pretrained layers.
    top_model = conv_base.output
    top_model = Flatten(name="flatten")(top_model)
    if n_model == 1 or n_model == 2:
        top_model = Dense(4096, activation='relu')(top_model)
        top_model = Dense(1072, activation='relu')(top_model)


    if n_model == 3 or n_model == 4:
        top_model = Dense(4096, activation='relu')(top_model)
        top_model = Dense(1024, activation='relu')(top_model)
        top_model = Dense(256, activation='relu')(top_model)
        top_model = Dense(64, activation='relu')(top_model)

    if n_model == 5:   
     top_model = Dense(4096, activation='relu')(top_model)
     top_model = Dense(2048, activation='relu')(top_model)
     top_model = Dense(1024, activation='relu')(top_model)
     top_model = Dense(512, activation='relu')(top_model)
     top_model = Dense(256, activation='relu')(top_model)
     top_model = Dense(128, activation='relu')(top_model)
     top_model = Dense(64, activation='relu')(top_model)
     top_model = Dense(32, activation='relu')(top_model)
    
    top_model = Dropout(0.2)(top_model)
    output_layer = Dense(n_classes, activation='softmax')(top_model)
    
    # Group the convolutional base and new fully-connected layers into a Model object.
    model = Model(inputs=conv_base.input, outputs=output_layer)

    # Compiles the model for training.
    model.compile(optimizer=optimizer, 
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def train_valid_generator(n_model, train_data, class_subset, BATCH_SIZE):
    if n_model == 1:
        train_generator = ImageDataGenerator(
                    validation_split=0.15,
                    fill_mode='nearest',
                    preprocessing_function=preprocess_input
                ) 
    
    else:
        train_generator = ImageDataGenerator(
            brightness_range=[0.5, 1.5],
            width_shift_range=0.1, 
            height_shift_range=0.1,
            zoom_range=[0.95, 1.05],
            validation_split=0.15,
            fill_mode='nearest',
            preprocessing_function=preprocess_input
        )
              
    traingen = train_generator.flow_from_directory(train_data,
                                                target_size=(224, 224),
                                                class_mode='categorical',
                                                classes=class_subset,
                                                subset='training',
                                                batch_size=BATCH_SIZE, 
                                                shuffle=True,
                                                seed=42)

    validgen = train_generator.flow_from_directory(train_data,
                target_size=(224, 224),
                class_mode='categorical',
                classes=class_subset,
                subset='validation',
                batch_size=BATCH_SIZE,
                shuffle=True,
                seed=42)            
    return traingen, validgen

def plot_heatmap(y_true, y_pred, class_names, ax, title):
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(
        cm, 
        annot=True, 
        square=True, 
        xticklabels=class_names, 
        yticklabels=class_names,
        fmt='d', 
        cmap=plt.cm.Blues,
        cbar=False,
        ax=ax
    )
    ax.set_title(title, fontsize=24)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylabel('True Label', fontsize=20)
    ax.set_xlabel('Predicted Label', fontsize=20)


def add_value_labels(ax, spacing=5):

    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.