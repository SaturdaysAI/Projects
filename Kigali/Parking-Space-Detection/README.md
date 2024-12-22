# IntelligentSystemforParkingSpaceDetection

IntelligentSystemforParkingSpaceDetection is an intelligent parking space detection system that uses computer vision and machine learning to analyze parking lot occupancy in images and videos. This application helps urban planners, parking lot managers, and drivers optimize parking space utilization and reduce traffic congestion.

## Features

- User authentication system for secure access
- Image analysis for parking space detection
- Video processing for real-time parking space monitoring
- Visualization of empty and filled parking spaces
- Count display for empty and filled parking spaces
- Web-based interface using Streamlit

## Technology Stack

- Python 3.8+
- Streamlit for the web interface
- OpenCV (cv2) for image and video processing
- PyTorch and YOLO for object detection
- SQLite for user authentication database
- NumPy for numerical operations
- Matplotlib and scikit-learn for data visualization and analysis

## Installation

1. Clone the repository:

   ```
   git clone <REPOSITORY_URL>
   cd <PROJECT_NAME>
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Download the YOLO model weights and place them in the `./model/` directory.

## Usage

1. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Sign up for a new account or log in if you already have one.

4. Upload an image or video of a parking lot.

5. Click the "Analyze Parking Spaces" button to process the image or video.

6. View the results, including the visualized parking spaces and occupancy counts.

## How It Works

1. **User Authentication**: The app uses SQLite to store user credentials securely. Passwords are hashed for additional security.

2. **Image Processing**:

   - The app uses a YOLO (You Only Look Once) model trained on parking lot data to detect parking spaces.
   - It classifies spaces as empty or filled and draws bounding boxes around them.
   - The processed image is displayed with color-coded boxes (green for empty, red for filled) and occupancy counts.

3. **Video Processing**:

   - For video input, the app processes frames at regular intervals.
   - It displays the processed frames in real-time, showing parking space detection and occupancy changes over time.

4. **Visualization**:
   - The app uses OpenCV to draw angled corner boxes around detected parking spaces.
   - Text overlays provide information about empty and filled space counts.

## Known Issues

### Missing Modules for Full Functionality

While deploying the application, you may encounter errors due to missing modules or dependencies. These issues occur because certain modules referenced in the code are not included in the current project setup. These modules are non-essential for the core functionality of the application but can prevent it from running as expected.

### Temporary Solution

To temporarily resolve this issue and deploy the application, you can remove or comment out the calls to the missing modules in the code. These modules are not critical for features such as parking space detection and analysis.

#### Steps to Apply the Temporary Fix:

1. Open the project files in your code editor.
2. Locate the lines where the missing modules are imported or called.
3. Comment out or delete these lines.

## Contributing

Contributions to IntelligentSystemforParkingSpaceDetection are welcome! Please feel free to submit pull requests, create issues or spread the word.

## Contact

Emmanuel SHYIRAMBERE - emashyirambere1@gmail.com
MAOHORO MPAKANYI Florien - mahorompakanyiflorien@gmail.com

Project Link: https://github.com/EmmanuelSHYIRAMBERE/UrbanTrafficOptimizer
