import tensorflow as tf
# Check your tensorflow version.
print(tf.__version__)

# If it's 2.15, run the following
'''
# Uninstall Tensorflow v2.15 and install v2.16.1
!pip uninstall tensorflow -y
!pip install tensorflow==2.16.1
'''

# Run this if it's your first time. 
# The system needs to install gradio to generate the interface.
# !pip install gradio

import os
import json
import tensorflow as tf
import gradio as gr
import numpy as np
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image

# Here we load our project folder, that has the following structure:
# - root folder ("smartbite_project")
# |-- datasource
#   |-- food_info // Contains the nutritional information JSON file
#   |-- images // Contains all images
#   |-- meta // Contains metadata files, such as training & test data and classes
# |-- model
#   |-- model_trained_3class.keras // This is the model trained
# Change this path to the location of this project in your machine
base_folder = '../datasource'
model_name = '../model/model_trained_3class.hdf5'

# Read a JSON file and return its contents
def get_info_json(file):
  with open(file, "r", encoding="UTF-8") as f:
    info_food = json.load(f)
  return info_food

# Get the category name from the numeric representation returned by the model
def get_category(label_numeric, labels_strings_food):
  if label_numeric >= 0 and label_numeric < len(labels_strings_food):
    return labels_strings_food[label_numeric]

# Given an image, process it and make a prediction with the model
def predict_class(model, img):
  # Process image
  img = image.load_img(img, target_size=(299, 299))
  img = image.img_to_array(img)
  img = np.expand_dims(img, axis=0)
  img /= 255.

  # Generate prediction
  return np.argmax(model.predict(img))

def display_nutritional_information(imagen):
    prediction = predict_class(model, imagen)
    guessed_food = get_category(int(prediction), labels_strings_food)
    data = info_food[guessed_food]
    return "\n".join(f"{key}: {value}" for key, value in data.items())

# Load the trained model
model = models.load_model(model_name, compile=False)

# Get the nutritional information JSON file
info_food = get_info_json(os.path.join(base_folder, "food_info/food_info.json"))

# Store keys in a sorted array
labels_strings_food = []
for key in info_food:
    labels_strings_food.append(key)
labels_strings_food.sort()

demo = gr.Interface(
    fn=display_nutritional_information, # On image sent, run this fn
    inputs=gr.Image(type="filepath", label="Take a photo or upload a picture of your dish"),
    outputs=["text"],
    title="SmartBite",
    description="Upload a picture of your dish to see its nutritional information."
)

demo.launch()