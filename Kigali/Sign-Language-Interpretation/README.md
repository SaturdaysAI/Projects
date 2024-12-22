# Sign Language Recognition

This project aims to provide a sign language recognition system using a deep learning model and a Flask web application. The application captures video from the user's webcam, processes hand gestures, and translates them into text, allowing real-time communication in sign language.

## Features

- **Gesture Recognition**: Real-time detection of hand gestures and their translation into sign language letters.
- **Web Interface**: A user-friendly interface accessible through a web browser.

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

3. **Download the Model**:  
   Ensure the model file `model.pt` is placed in the project directory.

4. **Run the Application**:
    ```bash
    python app.py
    ```

5. **Test the Application**:
   Interact with the app through the browser interface and test sign language recognition using your webcam.

## Usage

1. **Launch the App** by running `app.py`.
2. **Access it via your browser**: `http://localhost:5000/`.
3. **Perform Gesture Recognition**: The webcam will automatically detect hand gestures, translating them into sign language letters.
