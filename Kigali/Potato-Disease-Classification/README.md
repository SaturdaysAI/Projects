# Potato Disease Classification

This project aims to help farmers reduce economic losses by identifying potato leaf diseases using Convolutional Neural Networks (CNNs). The application was developed with TensorFlow for model building and Streamlit for deployment. The dataset used is [Plant Village Dataset](https://www.kaggle.com/datasets/arjuntejaswi/plant-village) which includes images of various plant diseases.

## Features
- Identifies potato leaf diseases as one of the following:
  - Potato___Early_blight
  - Potato___Late_blight
  - Potato___healthy

## Current Limitations
This repository is incomplete and cannot be executed as is. The code references a machine learning model (`Potato_model.hdf5`) that is not included in the uploaded files. Without this file, the application cannot load the model required for predictions.

## Running the Project (Once Complete)
After adding the missing model file, follow these steps:

1. Install the required dependencies:
   ```bash
   pip install streamlit tensorflow pillow numpy
   ```
2. Run the application using Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Open the provided URL (e.g., `http://localhost:8501`) in your web browser to interact with the app.
