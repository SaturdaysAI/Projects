import os
import math
import json
import numpy as np
import pandas as pd
from tensorflow.keras import models
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_folder = '../datasource'
model_name = '../model/model_trained_3class.hdf5'
images_dir = os.path.join(base_folder,"images")


test_data = json.load(open(os.path.join(base_folder,"meta/test.json")))

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

# Dataset for validation
df_test = create_dataframe(test_data)

img_width, img_height = 299, 299

# We create an ImageDataGenerator for test and training data
datagen = ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2
)

# We use the JSON files and folders to create the generator
test_generator = datagen.flow_from_dataframe(
    df_test,
    directory=images_dir,
    x_col='filename',
    y_col='label',
    class_mode='categorical',
    target_size=(img_height, img_width),
)

batch_size = 32


# Load the trained model
model = models.load_model(model_name)
model.compile(
    optimizer=SGD(learning_rate=0.0001, momentum=0.9),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

score = model.evaluate(test_generator, steps=math.ceil(len(df_test) / batch_size), verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Metrics')
print(score)