# Real-Time Deepfake Voice Detection for Voice Calls

This project is part of the **AI Saturdays Kigali** program and aims to develop a deep learning model capable of distinguishing between real and fake (deepfake) voice recordings. The application is designed to analyze voice data in real-time, providing reliable detection results.

## Features

- **Deepfake Detection**: Identify whether a given voice recording is real or generated using deepfake technology.
- **User-Friendly Interface**: Accessible via a web application built with Flask.  

## Installation

### Prerequisites

- **Python 3.9+**
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

3. **Run the Application**:
    ```bash
    python app.py
    ```

4. **Test the Application**:
   Interact with the app via your local server and test with voice recordings.

## Usage

1. **Launch the App** by running `app.py`.
2. **Access it via your browser**: `http://localhost:5000/`.
3. **Upload Voice Data**: Provide a voice recording for analysis.
4. **View Results**: The application will display whether the input is a real or deepfake voice.
