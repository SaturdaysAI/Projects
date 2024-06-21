# Dementia Prediction from MRI Images using OASIS Dataset
## Overview

This project provides a system for predicting dementia from MRI images using a combination of convolutional neural networks (CNN) and random forest classifiers. The system processes MRI images to predict dementia, ensuring a non-discriminatory and privacy-conscious approach. It utilizes a CNN to extract dementia probabilities for each MRI image type, and these probabilities are then combined and enhanced using a random forest model to provide robust and accurate predictions.
 <!-- Add a relevant image in the `docs` folder -->
## Key Features

* A set of Convolution Neural Networks process MRI images to extract dementia probabilities for different image types.
* Combines the CNN outputs to form a comprehensive prediction model using a random forest classifier.
* Ensures privacy by optionally not requiring personal demographic data.
* Does not require high computational resources, able to be run on laptops or on Colab.
## Collaborators
This project was made in the Saturdays AI Asturias course by group 1 in 2024, by:

* Francisco José Álvarez
* Bárbara Llano Ventoso
* Hugo Enrique Arteaga Vivas
* Jesús Andrés Lorenzana
* Pablo García García

## Origin of Data
This project uses data from ([OASIS-1 DATASET](https://sites.wustl.edu/oasisbrains/)) aimed at making neuroimaging datasets freely available to the scientific community. This set consists of a cross-sectional collection of 416 subjects aged 18 to 96. For each subject, 3 or 4 individual T1-weighted MRI scans obtained in single scan sessions are included. The subjects are all right-handed and include both men and women. 100 of the included subjects over the age of 60 have been clinically diagnosed with very mild to moderate Alzheimer’s disease (AD). 

As the Dataset is large and uses 3D brain scans, .jpg slices for each of the image types and subjects were extracted, for a total of 5 different brain MRI images for each subject
For easier access all images and subject data are already loaded into a [Dictionary](save_dict3_decompressed.p) so that only loading of a single file is needed to use the entire dataset. To create the dictionary, one can also run [Script](transform_images.py)


![Alt text](docs/brain_image.png?raw=true "Brain Image")
## Installation
If you have a CUDA device, you can always run the command ` pip install -r requirements.txt`. Else basic libraries are Pytorch, Optuna, Matplotlib, Scipy, Scikit-Learn, Pandas
You can always clone the repository with and all commands must be run from  [Main File](saturdays-dementia_main.py)
```
!git clone https://github.com/bloodclaw2000/Dementia_OASIS_Saturdays.git

```
There is also an available Colab repository for fully online integration.  [Colaboratory File](dementia_colab.ipynb)
## Usage
First we need to load the dictionary and create the Neural Network object, wich will handle all dataset splitting and training:
```
compressed_pickle_directory = "save_dict3"
tmp_dict = decompress_pickle('{0}.pbz2'.format(compressed_pickle_directory))
torch.set_default_device(device)
logpath = 'logs/'
obj = Dementia(dictionary=tmp_dict, device=device)
```
Code is Modular, You can leave commented any of the following lines without breaking the program as it saves results to disk.

To train the neural netwok with hyperparameters set at params_nn and for each of the image types ('T88', 'FSL'...) and saves them to a folder in nn/
```
train_nn(obj, 'params_nn/', ['T88', 'FSL', 'RAW_1', 'RAW_2', 'RAW_3'],logpath = logpath)
```
To create the predictions from the neural networks and write them to a csv file:
```
getOutput('nn/', ['T88', 'FSL', 'RAW_1', 'RAW_2', 'RAW_3'],device = device)
```
You can now train and test a Random Forest model. Choosing of usable params are in treeparam/. You can decide to use identiying data from the parameter file
```
source_df = pd.read_csv('results.csv')
treeclass = Customtree(source_df)
train_tree(treeclass,'params_tree/treeparam.txt')
```
For hyperparameter optimization, two approachs were used. For an Optuna Sampler approach:
```
find_hyperparams_optuna(obj, 'params_nn/','hyperparams/','studies/','dataset/', ['RAW_1','RAW_2','RAW_3','T88'],logpath = logpath, n_trials= 200)
visualizeresults('studies/RAW_1.pbz2')
```
For a brute search write:
```
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
train_nn_auto(obj, 'params_nn/', ['FSL'],logpath = logpath,experiments=parameter_ranges_FSL,max_iterations_ximage=100)
```
## Results
Parameter importance after optimization with Optuna:

<img src="docs/param_importances.jpg?" width="400" height="400">

Confusion Matrix from two neural networks showing acceptable predictions of Dementia for different image types

<img src="docs/FSL_SEG_1_confusion_matrix.png?" width="400" height="400"> <img src="docs/RAW_2_confusion_matrix.png?" width="400" height="400">

Confusion Matrix from FSL_SEG and RAW_2 MRI Images

Confusion Matrix in same dataset split after training with Random Forest using only NN predictions
![Alt text](docs/forest_confusion_matrix.png?raw=true "Brain Image")

