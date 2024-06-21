# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 22:04:40 2024

@author: Pablo
"""
import os
import numpy as np
from PIL import Image
import cv2
import scipy
import sys
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import time
import pickle
import _pickle as cPickle
import bz2
import csv


def load_images(root_dir, csv_path, save=False, plot=True, save_dict=False):
    """
    This function takes a root_dir parameter, which is the directory where the MRI images are stored. If plot is set to True, it will also display plots of the original and transformed images. It returns a dictionary containing the loaded images organized by subject ID, session, folder, and slice number.

    Parameters
    ----------
    root_dir : TYPE
        DESCRIPTION.
    plot : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    image_dict : TYPE
        DESCRIPTION.

    """

    image_dict = {}

    for folder, subfolders, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.jpg') and file.startswith('OAS1'):
                filename_parts = file.split('_')
                print(filename_parts[0:2])
                subject_id = filename_parts[1]
                subject_session = filename_parts[2]
                folder_parts = folder.split('\\')
                folder_important = folder_parts[-1]
                # print(folder_important)
                key1 = f"{subject_id}"
                if key1 not in image_dict:
                    image_dict[key1] = {}
                # now we want to separate sessions on same subject
                key2 = f"{subject_session[2:]}"
                # print(key2)
                if key2 not in image_dict[key1]:
                    image_dict[key1][key2] = {}
                key3 = f"{folder_important}"  # RAW, T88, etc
                if key3 not in image_dict[key1][key2]:
                    image_dict[key1][key2][key3] = {}
                # here we load the image
                image_path = os.path.join(folder, file)
                image_array = np.array(Image.open(image_path))

                if len(image_array.shape) == 3:
                    """ if the image is in RGB, we only get one color (intensity)
                    this is technically correct as the change from gif to jpg
                    is only for intensities as MRI only gets those"""
                    image_array = image_array[:, :, 0]
                    # brain_fft = brain_fft.astype('float32')
                key4 = 1  # this so it is always a new image, inside folder
                while True:
                    if key4 not in image_dict[key1][key2][key3]:
                        image_dict[key1][key2][key3][key4] = {}
                        image_dict[key1][key2][key3][key4]["original"] = image_array
                        """now we do the transformations add here as we add more transformations
                            Currently Supported:
                                FFT
                                Border

                        """
                        """
                        # we do a fourier transform
                        fft_array = fft_transform(image_array)
                        edge_array = border_transform(image_array)
                        image_dict[key1][key2][key3][key4]["fft"] = fft_array
                        # we find the borders of the image
                        image_dict[key1][key2][key3][key4]["borders"] = edge_array
                        # we
                        """
                        if plot:
                            plt.figure()
                            fig, ax = plt.subplots(1, 3, figsize=(15, 5))
                            ax[0].imshow(image_array)
                            ax[0].set_title('Original MRI')
                            ax[1].imshow(fft_array)
                            ax[1].set_title('fft Transform')
                            ax[2].imshow(edge_array)
                            ax[2].set_title('edges')
                            plt.show()
                        if save:
                            transformed_image_path = os.path.splitext(image_path)[
                                0] + '.txt'
                            transformed_image_fft_path = os.path.splitext(image_path)[
                                0] + '_fft.txt'
                            transformed_image_edge_path = os.path.splitext(image_path)[
                                0] + 'edges.txt'

                            # np.savetxt(transformed_image_path, image_array)
                            np.savetxt(transformed_image_fft_path,
                                       fft_array, fmt='%.8e')
                            np.savetxt(transformed_image_edge_path,
                                       edge_array, fmt='%d')
                        break
                    else:
                        key4 += 1
    # now we load csv file and add to dictionary
    csv_dict = load_csv(csv_path)
    for key in csv_dict:
        for keyc in csv_dict[key]:
            for keyy in csv_dict[key][keyc]:
                image_dict[key][keyc][keyy] = csv_dict[key][keyc][keyy]
    if save_dict:
        print("saving Pickle")
        #pet_save(image_dict)
        compressed_pickle(image_dict,saved_dict_path)
    return image_dict


def load_csv(file_path):
    csv_dict = {}
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        data = [row for row in csv_reader]
    for i in range(len(data)):
        filename_parts = data[i]['ID'].split('_')
        subject_id = filename_parts[1]
        subject_session = filename_parts[2][2:]
        key1 = subject_id
        key2 = subject_session
        if key1 not in csv_dict:
            csv_dict[key1] = {}
        if key2 not in csv_dict[key1]:
            csv_dict[key1][key2] = {}
            # now we load all data into the new dictionary
        for key in data[i]:
            # Use the key from the source dictionary to create a key in the destination dictionary
            # You can assign any value here if needed
            if key == 'ID':
                csv_dict[key1][key2][key] = key1
                continue
            if data[i][key] == 'N/A':
                csv_dict[key1][key2][key] = None
            else:
                csv_dict[key1][key2][key] = data[i][key]
    return csv_dict


def fft_transform(array):
    fourier_transform = scipy.fft.fft2(array)
    shifted_transform = scipy.fft.fftshift(fourier_transform)
    brain_fourier_powerspect = np.abs(shifted_transform) ** 2
    brain_fft = np.log10(brain_fourier_powerspect.real)
    brain_fft = brain_fft.astype('float16')
    # print(brain_fft.dtype)
    return brain_fft


def border_transform(array):
    # from Webology (ISSN: 1735-188X) Volume 19, Number 1, 2022
    edges = cv2.Canny(array, 80, 150)
    return edges


def pet_save(pet, filename):
    pickle.dump(pet, open(filename, "wb"))
# #guardamos en un binario

def compressed_pickle(data, filename):
    with bz2.BZ2File(f"{filename}" + '.pbz2', 'w') as f:
       cPickle.dump(data, f)


def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    # data = lzma.open(file, 'rb')
    data = cPickle.load(data)
    return data


"""
def border_transform_developing(gray_image):
    G1 = np.array([[1, 1], [-1, -1]])
    G2 = G1.transpose()
    # Üprint(gray_image.shape)
    Ix = convolve2d(gray_image, G1, mode="same")
    # print(Ix.shape)
    Iy = convolve2d(gray_image, np.transpose(G1), mode="same")

    def G(x, mean, std):
        return np.exp(-0.5*np.square((x-mean)/std))
    ux = G(Ix, 0, 50)

    uy = G(Iy, 0, 50)

    rows, cols = ux.shape

    def inference(gray_image, ux, uy):
        Iinf = np.zeros(list(gray_image.shape), dtype='float')
        for i in range(ux.shape[0]):
            for j in range(ux.shape[1]):
                if(ux[i][j] >= 0.8 and uy[i][j] >= 0.8):
                    Iinf[i][j] = min(ux[i][j], uy[i][j])

        return Iinf

    def defuzzification(gray_image, ux, uy):
        rows, cols = ux.shape
        Idef = np.empty(list(gray_image.shape), dtype='float')
        for i in range(rows):
            for j in range(cols):
                if(ux[i][j] >= 0.8 and uy[i][j] >= 0.8):
                    Idef[i][j] = 255

        return Idef

    Iinf = inference(gray_image, ux, uy)
    Iout = defuzzification(gray_image, ux, uy)

    return Iout
"""


["fft", "border"]

root_directory = r"Raw_Data\oasis_processed"
csv_path = r"Raw_Data\oasis_cross-sectional.csv"
saved_dict_path = 'image_data3'
print("aa")
time1 = time.time()
image_dict = load_images(root_directory, csv_path, save=False,  # para cargar imagenes
                         plot=False, save_dict=True)
# para cargarlas desde el pickle
# image_dict = decompress_pickle('save_dict2.pbz2')

# para cargar el csv
# image_csv = load_csv(csv_path)
print(time.time()-time1, "s")
print("Size of dictionary in memory")
# print(sys.getsizeof(image_dict))
