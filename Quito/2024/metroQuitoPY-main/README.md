
# 🚇 Metro Quito + AI: Intelligent Video Processing Application

This is a Python-based desktop application that leverages AI-powered video processing to analyze train movements in Metro Quito. The application allows users to upload videos, define regions of interest (ROIs), and process these videos using advanced models like YOLOv8, resulting in an output video with the desired analytics.
![appDesktop](https://github.com/user-attachments/assets/dcc70776-bd44-4971-81e0-fdb50f122127)

---

## 📋 Features

- **Upload and Process Videos**: Users can upload videos of the Metro, define areas to track train movement, and process the video to analyze motion.
- **Interactive GUI**: Intuitive interface built with `Tkinter`, allowing users to interact with the application seamlessly.
- **AI-powered Analytics**: Utilizes YOLOv8 for object detection and tracking.
- **Cross-platform Support**: Build and run the application on both Linux and Windows.
- **Customizable Outputs**: Save processed videos to your preferred folder.

---

## ⚙️ Requirements

### System Requirements
- Python 3.10+
- GPU with CUDA support (optional, for faster video processing)
- Operating System:
  - Linux
  - Windows 10/11

### Python Dependencies
The required Python libraries are listed in `requirements.txt`. Some key dependencies include:
- `torch`
- `opencv-python`
- `ultralytics`
- `numpy`
- `matplotlib`

Install them using:

```bash
pip install -r requirements.txt
📂 Project Structure
bash
.
├── main_gui.py                   # Main file to run the application
├── models
│   └── yolov8
│       ├── yolov8n.pt           # YOLOv8 model file
│       ├── coco.names           # Class labels for YOLOv8
├── share                         # Utility functions and constants
├── requirements.txt              # Python dependencies
└── README.md                     # You're reading it now!
```

🚀 How to Run the Application

1️⃣ Clone the repository
```bash
git clone <repository-url>
cd metroQuitoPY
```
2️⃣ Set up the environment
Create and activate a virtual environment to isolate the dependencies:
```bash
# Linux
python3 -m venv venv
```

# Windows
python -m venv venv
venv\Scripts\activate
Install the dependencies:

```bash
pip install -r requirements.txt
```
3️⃣ Download YOLOv8 model and COCO names
Ensure the following files exist in models/yolov8:

yolov8n.pt
coco.names
4️⃣ Run the application
```bash
python main_gui.py
```

🏗️ Build an Executable (Optional)
If you'd like to create a standalone executable for the application:

Install PyInstaller:
pip install pyinstaller
Run the following command to create a single executable file:
```bash
pyinstaller --onefile --noconsole \
--add-data "models/yolov8/yolov8n.pt:models/yolov8" \
--add-data "models/yolov8/coco.names:models/yolov8" \
main_gui.py
```
The generated executable will be located in the dist/ directory.

Run the executable:
```bash
./dist/main_gui    # Linux
main_gui.exe       # Windows
```

🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

📄 License
This project is licensed under the MIT License.
