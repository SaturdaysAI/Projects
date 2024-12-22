from moviepy.editor import VideoFileClip
import librosa
import numpy as np
import torch
import os

# Preprocess audio file
def preprocess_audio(file_path):
    """Load and preprocess audio to be fed into the model."""
    audio, sr = librosa.load(file_path, sr=16000)  # Resample to 16kHz
    padded_audio = np.pad(audio, (0, max(0, 16000 * 3 - len(audio))))[:16000 * 3]  # Ensure 3 seconds
    audio_tensor = torch.tensor(padded_audio).float().unsqueeze(0)  # Add batch dimension
    return audio_tensor

# Extract audio from video
def extract_audio_from_video(video_path):
    """Extract audio from video and save it as a WAV file."""
    video = VideoFileClip(video_path)
    audio_file_path = video_path.rsplit('.', 1)[0] + '.wav'  # Save as .wav file
    video.audio.write_audiofile(audio_file_path, codec='pcm_s16le', fps=16000)
    return audio_file_path
