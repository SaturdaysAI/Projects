# Malaria-Infected Cell Detector

This project aims to develop a deep learning model capable of analyzing cell images to detect whether they are infected with malaria. The application leverages computer vision techniques to provide accurate and reliable results for medical image analysis.

## Features

- **Malaria Detection**: Classify cell images as either infected or uninfected by malaria parasites.  
- **High Accuracy**: The model is trained on a dataset of labeled cell images to ensure robust predictions.  
- **User-Friendly Interface**: Accessible via a web application built with Flask for seamless interaction.  

## Installation

### Prerequisites

- **Python 3.10+**
- **pip** (Python package installer)

### Setup

1. **Clone the Repository**:
    ```bash
    git clone <REPOSITORY_URL>
    cd <PROJECT_NAME>
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application using Streamlit**:
    ```bash
    streamlit run app.py
    ```

4. **Test the Application**:
   Interact with the app via your local server and upload cell images to test the malaria detection functionality.

## Usage

1. **Launch the App** by running `app.py`.
2. **Access it via your browser**: `http://localhost:8501/`.
3. **Upload Cell Images**: Provide microscopic cell images for analysis.
4. **View Results**: The application will display whether the uploaded cells are infected or uninfected by malaria.
