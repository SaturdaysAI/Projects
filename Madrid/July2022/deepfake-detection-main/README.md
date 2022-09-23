# DeepFake Detection with PyTorch 🧐

## Getting Started 🛠
🗂 Clone the repository (the command below uses HTTPS):
```sh
$ git clone https://github.com/aaronespasa/deepfake-detection.git
```

## Project Structure 🗂

```
deepfake-detection
│
└───dataset             # React component files
│   │   download.py     # Python script to download the dataset
│
data                    # The dataset will be stored here
│   │   ...
│
metrics                 # Metrics to be used in the model
│   │   ...
│
└───models              # Models to be used in the project
│   │   ...
│
└───saves               # Checkpoints & State Dicts of PyTorch
│   │   ...
│
└───utils               # Utility files (e.g. helper functions for visualization)
│   │   ...
│
│ training.py           # Python Script for training the model
│ training.ipynb        # Python Notebook for training the model
│
│ README.md
│ LICENSE  
│ gitignore  
```

## Set-Up Environment 🌲 
### Install the necessary dependencies
1. Install PyTorch and Cuda on a new conda environment ([PyTorch Anaconda commands](https://pytorch.org/get-started/locally/)):
```sh
$ conda create --name pytorch python=3.8
$ conda activate pytorch
$ conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

2. Install OpenCV:
```sh
$ pip install opencv-python
$ python -c "import cv2; print(cv2.__version__)"
```

3. Install Numpy, Matplotlib and Tqdm:
```sh
$ conda install -c conda-forge numpy matplotlib tqdm
```

4. Install Albumentations:
```sh
$ pip install albumentations
```

### Download the dataset
If you want to see the arguments that can be passed to download the dataset, run the following command:

```sh
$ python dataset/download.py -h
```

1. Download the FaceForensics++ dataset:
```sh
$ python dataset/download.py data -c c40 -d DeepFakeDetection
$ python dataset/download.py data -c c40 -d DeepFakeDetection_original
```
> Using -c c40 we get the maximum compression to download them fastly.

## Train the model 🛠
```sh
$ python training.py
```

## Roadmap

Binary Image Classifier:

- [x] Extract image frame from the videos.
- [x] Use a MTCNN to detect the faces and create a new dataset.
- [x] Filter the data (remove images which do not contain faces).
- [x] Data Augmentation.
- [x] Weights & Biases integration.
- [x] Binary Image Classifier of DeepFakes using a non-SOTA architecture (ex.: InceptionV3 or ResNet50).
- [ ] Binary Image Classifier of DeepFakes using a SOTA architecture (ex. Vision Transformers).
- [x] Evaluate the image classifier model using Class Activation Maps.
- [x] Model Deployment (for images) using Gradio.
- [x] Write an article describing the project.

Binary Video Classifier:

- [ ] Binary Video Classifier of DeepFakes.
- [ ] Evaluate the video classifier model using Class Activation Maps.
- [ ] Model Deployment (for videos) using Streamlit.
- [ ] Write an article describing how to improve the binary image classifier to work with video.

Binary Video Classifier including audio:
- [ ] Binary Classifier for DeepFakes using audio (implementing a Transformer architecture)
- [ ] Model evaluation.
- [ ] Model deployment using PyTorch Live.
- [ ] Write an article describing how to improve the binary video classifier to work with audio.
- [ ] Write a tutorial describing how to do the project.

## Dataset

[FaceForensics](http://niessnerlab.org/projects/roessler2018faceforensics.html): A Large-scale Video Dataset for Forgery Detection in Human Faces.

[FakeCatcher](http://cs.binghamton.edu/~ncilsal2/DeepFakesDataset/): Dataset of synthesized images for deepfake detection.

[Kaggle Dataset augmented by Meta](https://ai.facebook.com/datasets/dfdc/): Dataset from the kaggle competition with more resources provided by Meta.

## Presentation
https://docs.google.com/presentation/d/1Cj1c1Npyv3smCOE2v5zVS-LzkGSUkC61/edit?usp=sharing&ouid=103376187494457396648&rtpof=true&sd=true
