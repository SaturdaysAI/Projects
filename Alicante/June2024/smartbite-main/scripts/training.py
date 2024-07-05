import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger

# Here we load our project folder, that has the following structure:
# - root folder ("smartbite_project")
# |-- datasource // Contains the nutritional information JSON file
#   |-- food_info // Contains the nutritional information JSON file
#   |-- images // Contains all images
#   |-- meta // Contains metadata files, such as training & test data and classes
# |-- model
#   |-- model_trained_3class.keras // This is the model trained
# Change this path to the location of this project in your machine
base_dir = '../datasource/'

images_dir = os.path.join(base_dir,"images")

# This is a list of food that have a folder with the exact same name as it appears here. Eg.: "bread_pudding", "bruschetta", "caesar_salad"
with open(os.path.join(base_dir,"meta/classes.txt"), 'r') as f:
    food_folders = f.read().strip().split('\n')

# This is a list with the user-friendly name of the food in the same order as the previous file. Eg.: "Bread pudding", "Bruschetta", "Caesar salad"
with open(os.path.join(base_dir,"meta/labels.txt"), 'r') as f:
    food_names = f.read().strip().split('\n')

total_classes = len(food_folders)

train_data = json.load(open(os.path.join(base_dir,"meta/train.json")))
test_data = json.load(open(os.path.join(base_dir,"meta/test.json")))

def create_dataframe(data):
    X = []
    y = []
    for key in data:
      for item in data[key]:
          X.append(item.strip()+".jpg") # Image
          y.append(key.strip()) # Category
    X = np.array(X)
    y = np.array(y)
    df = pd.DataFrame()
    df['filename'] = X
    df['label'] = y
    return df

# Dataset for training
df_train = create_dataframe(train_data)
# Dataset for validation
df_test = create_dataframe(test_data)

img_width, img_height = 299, 299

# We create an ImageDataGenerator for test and training data
datagen = ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2
)

# We use the JSON files and folders to create the generator
train_generator = datagen.flow_from_dataframe(
    df_train,
    directory=images_dir,
    x_col='filename',
    y_col='label',
    class_mode='categorical',
    target_size=(img_height, img_width),
)

test_generator = datagen.flow_from_dataframe(
    df_test,
    directory=images_dir,
    x_col='filename',
    y_col='label',
    class_mode='categorical',
    target_size=(img_height, img_width),
)

batch_size = 32

# Initialize the pretrained Model
inception = tf.keras.applications.inception_v3.InceptionV3(weights='imagenet', include_top=False)

# Set layers
x = inception.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)

predictions = Dense(
    total_classes,
    kernel_regularizer=regularizers.l2(0.005),
    activation='softmax'
)(x)

# Create model & compile it
model = Model(inputs=inception.input, outputs=predictions)
model.compile(
    optimizer=SGD(learning_rate=0.0001, momentum=0.9),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Add checkpoints, store only the best model in each epoc
checkpointer = ModelCheckpoint(
    filepath='best_model.keras',
    verbose=1,
    save_best_only=True
)

csv_logger = CSVLogger('history.log')

# Train the model with data (each epoc took ~9h, so I suggest you to skip this step :P)
history = model.fit(
    train_generator,
    validation_data=test_generator,
    batch_size=batch_size,
    epochs=30,
    verbose=1,
    callbacks=[csv_logger, checkpointer])

# Uncomment this if you need to continue the training after stopping it
'''
# Load the last (best) version of the model we have
model = load_model('best_model.keras')

# Load the training history
history_df = pd.read_csv('history.log')

# Get the number of epoch completed
initial_epoch = len(history_df)

# Set the checkpoints up again, we still want to save the best models from next epochs
checkpointer = ModelCheckpoint(filepath='best_model.keras', verbose=1, save_best_only=True)
csv_logger = CSVLogger('history.log', append=True)

# Continue training the model
history = model.fit(train_generator,
    validation_data=test_generator,
    batch_size=batch_size,
    initial_epoch=initial_epoch, # Continue from last epoch
    epochs=30,
    verbose=1,
    callbacks=[csv_logger, checkpointer])
'''

# Save the entire model as a SavedModel.
model.save('model_trained.keras')