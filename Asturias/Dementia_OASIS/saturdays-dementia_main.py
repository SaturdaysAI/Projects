import os
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import sys
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import pickle
import _pickle as cPickle
import bz2
import csv
import torch
import torchvision
from torch.utils.data import Dataset
from torch import nn
from torch.utils.data import DataLoader
import torch.optim as optim
from torchvision import datasets, transforms
import torch.nn.functional as F
import random
from tabulate import tabulate
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
# from sklearn.tree import export_graphviz
from IPython.display import Image
# import graphviz
from sklearn import tree

from pickle_aux import pet_load, decompress_pickle, pet_save
from dementia_network_class import Dementia, train_nn, train_nn_auto, getOutput
from dementia_tree_class import train_tree,  Customtree
from hyperparameter_optimization import get_optimal_params, find_hyperparams_optuna, visualizeresults

import time
"""
Version 2.0.2 of Project
28/05/2024
"""
torch.multiprocessing.set_start_method(
    'spawn', force=True)  # kinda important mostly for CPU

device = torch.device(
    f'cuda:{torch.cuda.current_device()}'
    if torch.cuda.is_available()
    else 'cpu')


# pickle_directory = f"/content/drive/MyDrive/grupo1-saturdaysAI/data/save_dict3.p"
compressed_pickle_directory = "save_dict3"
if not os.path.exists('{0}_decompressed.p'.format(compressed_pickle_directory)):
    def force_dementia(dictionary):
        for key in dictionary:
            for key2 in dictionary[key]:
                if dictionary[key][key2]['CDR'] == '':
                    dictionary[key][key2]['Dementia'] = 0
                elif float(dictionary[key][key2]['CDR']) > 0:
                    dictionary[key][key2]['Dementia'] = 1
                else:
                    dictionary[key][key2]['Dementia'] = 0
        return dictionary

    def removeyoung(dictionary, age):
        dic_pacientes_viejos = {}
        for key in dictionary:
            for key2 in dictionary[key]:
                if int(dictionary[key][key2]['Age']) >= age:
                    dic_pacientes_viejos[key] = dictionary[key]
        return dic_pacientes_viejos

    tmp_dict = decompress_pickle(
        '{0}.pbz2'.format(compressed_pickle_directory))
    tmp_dict = force_dementia(tmp_dict)  # esto es la funcion del init
    tmp_dict = removeyoung(tmp_dict, 59)
    tmp_dict = {int(key): value for key, value in tmp_dict.items()}
    new_dict = {}
    current_index = 0
    for key in sorted(tmp_dict.keys()):
        new_dict[current_index] = tmp_dict[key]
        current_index += 1
    tmp_dict = new_dict

    pet_save(tmp_dict, '{0}_decompressed.p'.format(
        compressed_pickle_directory))
else:
    tmp_dict = pet_load('{0}_decompressed.p'.format(
        compressed_pickle_directory))

def createnecessaryfolders():
    if not os.path.exists(f"plots/"):
        os.makedirs(f"plots/")
    if not os.path.exists(f"studies/"):
        os.makedirs(f"studies/")
    if not os.path.exists(f"params_nn/"):
        os.makedirs(f"params_nn/")
    if not os.path.exists(f"nn/"):
        os.makedirs(f"nn/")
    if not os.path.exists(f"logs/"):
        os.makedirs(f"logs/")
    if not os.path.exists(f"hyperparams/"):
        os.makedirs(f"hyperparams/")
    if not os.path.exists(f"dataset/"):
        os.makedirs(f"dataset/")
    if not os.path.exists(f"params_tree/"):
        os.makedirs(f"params_tree/")
# device = "cpu"

# we create a random seed and torch random generator:


torch.set_default_device(device)

print(f" Using {device} in this run")

logpath = 'logs/'
createnecessaryfolders()
obj = Dementia(dictionary=tmp_dict, device=device)



# Podemos setear los parámetros para el entrenamiento aquí:
obj.setParam('image_type', 'T88_111')
obj.setParam('image_number', 1)

# print(tabulate(source_df, headers="keys", tablefmt="grid"))



time1 = time.time()

parameter_ranges_FSL = {
    'patience_validation': [1],
    'patience_plateau': [0],
    'delta_min': [0.1],
    'batch_size': [30, 40, 50],
    'split_size': [0.8],
    'max_loss_reset': [1],
    'learning_rate': [0.00001,0.00005, 0.00008,0.0001],
    'weight_decay': [0.03, 0.01, 0.02],
    'first_conv_outchann': [10,12],
    'second_conv_outchann': [24],
    'fclayer1': [210],
    'fclayer2': ['None'],
    'optimizer': ['Adam']
}
parameter_ranges_T88 = {
    'patience_validation': [0],
    'patience_plateau': [1],
    'delta_min': [0.1],
    'batch_size': [30, 40, 50],
    'split_size': [0.8],
    'max_loss_reset': [1],
    'learning_rate': [0.001,0.0009, 0.0012,0.0015],
    'weight_decay': [0.008, 0.01, 0.02],
    'first_conv_outchann': [12],
    'second_conv_outchann': [20],
    'fclayer1': [180],
    'fclayer2': [30],
    'optimizer': ['Adam']
}
parameter_ranges_RAW_1 = {
    'patience_validation': [2],
    'patience_plateau': [0],
    'delta_min': [0.1],
    'batch_size': [30, 40, 50],
    'split_size': [0.8],
    'max_loss_reset': [1],
    'learning_rate': [0.00012,0.00005, 0.00008,0.0001],
    'weight_decay': [0.016],
    'first_conv_outchann': [10,12],
    'second_conv_outchann': [24],
    'fclayer1': [210],
    'fclayer2': ['None'],
    'optimizer': ['Adam']
}
parameter_ranges_RAW_2 = {
    'patience_validation': [1],
    'patience_plateau': [1],
    'delta_min': [0.1],
    'batch_size': [30, 40, 50],
    'split_size': [0.8],
    'max_loss_reset': [1],
    'learning_rate': [0.0001,0.0005, 0.0002,0.0003],
    'weight_decay': [0.03, 0.01, 0.02],
    'first_conv_outchann': [10,12],
    'second_conv_outchann': [24],
    'fclayer1': [210],
    'fclayer2': ['None'],
    'optimizer': ['Adam']
}
parameter_ranges_RAW_3 = {
    'patience_validation': [1],
    'patience_plateau': [0],
    'delta_min': [0.1],
    'batch_size': [30, 40, 50],
    'split_size': [0.8],
    'max_loss_reset': [1],
    'learning_rate': [0.00001,0.00005, 0.00008,0.0001],
    'weight_decay': [0.03, 0.01, 0.02],
    'first_conv_outchann': [10,12],
    'second_conv_outchann': [24],
    'fclayer1': [210],
    'fclayer2': ['None'],
    'optimizer': ['Adam']
}


if os.path.exists('tmp_nn.p'):
    obj = pet_load('tmp_nn.p')
    print(f"USing old unfinished dataset split with seed {obj.seed}")
#Decomment from here what you want to use

#using Optuna to find optimal hyperparameters given ranges in hyperparams forlder
#find_hyperparams_optuna(obj, 'params_nn/','hyperparams/','studies/','dataset/', ['RAW_1','RAW_2','RAW_3','T88'],logpath = logpath, n_trials= 200)

#allows to visualize Optuna Studies Results
visualizeresults('studies/T88.pbz2')


#to train a neural network from params_nn files or various at the same time
#train_nn(obj, 'params_nn/', ['T88', 'FSL', 'RAW_1', 'RAW_2', 'RAW_3'],logpath = logpath)
# train_nn(obj, 'params_nn/', ['T88'],logpath = logpath)

#hyperoptimize from parameter_ranges

#train_nn_auto(obj, 'params_nn/', ['T88'],logpath = logpath,experiments=parameter_ranges_T88,max_iterations_ximage=100)
#train_nn_auto(obj, 'params_nn/', ['RAW_1'],logpath = logpath,experiments=parameter_ranges_RAW_1,max_iterations_ximage=100)
#train_nn_auto(obj, 'params_nn/', ['RAW_2'],logpath = logpath,experiments=parameter_ranges_RAW_2,max_iterations_ximage=100)
#train_nn_auto(obj, 'params_nn/', ['RAW_3'],logpath = logpath,experiments=parameter_ranges_RAW_3,max_iterations_ximage=100)
#train_nn_auto(obj, 'params_nn/', ['FSL'],logpath = logpath,experiments=parameter_ranges_FSL,max_iterations_ximage=100)


# para llamar al optimizador sin entrenar
# df = pd.read_csv('_T88.csv')
# get_optimal_params(df)


print(f"Normal network running time",time.time()- time1, 's')

#gets a csv with all data and predictions from the Neural Networks for the random forest
#getOutput(tmp_dict,'nn/', ['T88', 'FSL', 'RAW_1', 'RAW_2', 'RAW_3'],device = device)

#creates the random forest and trains  it 
source_df = pd.read_csv('results.csv')
treeclass = Customtree(source_df)
#treeclass.write_dict_to_file('params_tree/treeparam.txt')
train_tree(treeclass,'params_tree/treeparam.txt')
