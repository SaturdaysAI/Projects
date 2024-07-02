<p align="center">
  <img width="1200"  src="https://imagizer.imageshack.com/img923/6061/5ZhKpP.jpg" alt="infarction prediction banner">
</p>

# Infarction Prediction

## Project overview

**Infarction Prediction** is an AI-powered tool designed to predict heart attacks (myocardial infarction) using ECG images. The main goal of this project is to provide emergency medical personnel with a quick and reliable tool for early detection of heart attacks, potentially saving lives through timely intervention.


## Dataset

For training the model, we utilized the [**PTB-XL dataset**](https://physionet.org/content/ptb-xl/1.0.3/), which comprises 21,837 clinical ECG records from 18,885 patients. Each record consists of 12-lead ECGs lasting 10 seconds.

## File descriptions

- **exploration_notebook.ipynb**: Exploratory Data Analysis (EDA)
- **data_loading_utils.py**: Data preprocessing utilities
- **model_training.ipynb**: Model training notebook
- **models/standard_scaler.pkl**: Data normalizer
- **models/cnn_model.h5**: Trained CNN model
- **app.py**: Interface for predicting infarction by uploading an ECG image
- **ecg.py**: A set of functions for processing ECG images and predicting myocardial infarction
- **requirements.txt**: Required libraries for running the project


## How to run the project

### Using Docker

To run the Dockerized version of the project, follow these steps:

1. Ensure you have Docker installed: If you don't have Docker installed, you can download and install it from [Docker's official website](https://www.docker.com/get-started/).

   
2. Pull the Docker image from Docker Hub:
  ```bash
  docker pull gala1812/infarction-prediction:latest
  ```

3. Run the Docker container:
  ```bash
  docker run -p 8501:8501 gala1812/infarction-prediction:latest
  ```

4. Access the application: Open your web browser and navigate to http://localhost:8501.
  You should see the Streamlit application interface where you can upload an ECG image to get the prediction.

### Without Docker

1. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Upload an ECG image to get the prediction.

### Try it on your phone

Access the application: open your phone's web browser and navigate to:
https://infarction-prediction-saturdays.streamlit.app/

You should see the responsive Streamlit app interface, where you can upload an image or take a mobile photo of an ECG to get the prediction.

## Authors

This project was created by a team from the 7th edition of Saturdays.AI Madrid:

- [Gabriela Calzadilla Rodriguez](https://www.linkedin.com/in/gabrielacalzadilla/)
- [Galyna Chupirova](https://www.linkedin.com/in/galyna-chupirova-447b6142/)
- [Karla Lamus Oliveros](https://www.linkedin.com/in/karla-lamus/)
- [Nicolás Martínez-Geijo Vila](https://www.linkedin.com/in/nicolasgeijo/)
- [Paloma García García de Castro](https://www.linkedin.com/in/paloma-garcia-data-science/)
