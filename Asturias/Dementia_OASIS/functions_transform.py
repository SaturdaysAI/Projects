import scipy
import numpy as np
import cv2

# Métodos Transformciones


def fft_transform(array):
    fourier_transform = scipy.fft.fft2(array)
    shifted_transform = scipy.fft.fftshift(fourier_transform)
    brain_fourier_powerspect = np.abs(shifted_transform) ** 2
    brain_fft = np.log10(brain_fourier_powerspect.real)
    brain_fft = brain_fft.astype('float32')
    # print(brain_fft.dtype)

    return brain_fft


def border_transform(array):
    # from Webology (ISSN: 1735-188X) Volume 19, Number 1, 2022
    edges = cv2.Canny(array, 80, 150)
    return edges
