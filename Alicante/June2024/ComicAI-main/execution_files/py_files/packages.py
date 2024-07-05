import fitz  # PyMuPDF
import os
import csv
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import easyocr
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from deep_translator import GoogleTranslator
from gtts import gTTS
from pathlib import Path
from moviepy.editor import AudioFileClip, concatenate_audioclips