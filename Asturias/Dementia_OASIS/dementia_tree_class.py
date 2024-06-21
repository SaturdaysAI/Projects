# -*- coding: utf-8 -*-
"""
Created on Thu May 23 18:27:27 2024

@author: Pablo
"""

import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from misc_aux import dropparameters
from sklearn import tree




def train_tree(obj, filepath):
    """
     Train the neural network on the files in the folder_path and write the predictions to the output

     Args:
         obj: The object to use for training
         folder_path: The folder where the files are to be read
         process_files: A list of files to process or
    """
    if os.path.isfile(filepath) and 'output' not in filepath and 'skip' not in filepath:
        obj.read_params_from_file_and_set(filepath)
        print(f"Now calculating predictions for file {filepath}")
        # Get the basename with extension
        file_basename = os.path.basename(filepath)
        file_without_extension = os.path.splitext(file_basename)[0]
        # Open the file in write mode ('w')
        print(obj.trainParam)
        obj.trainandtest()

# Custom tree classificator:


class Customtree:

    def __init__(self, dataset):
        """
          Initialize the class. This is the method that must be called by the user to initialize the class

          Args:
                   dictionary: Dictionary containing the parameters needed to train the model
                   device: Device on which to run the model.
                   generator: Random number generator to use
                   seed: Random seed
        """

        self.source_df = dataset
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.rf = None
        self.clf = None

        self.trainParam = {
            'plot': True,
            'estimators': 200,
            'max_depth': 5,
            'criterion': 'gini',
            'optimize': True,
            'use_identifying_data': False,  # use age, economy eductation etc
            'use_mri_data': True,  # uses the neural network outputs
            'use_brain_size_data': True,  # uses the ASF eTIV ASF
            'age': True,  # if identifying data true, cal select wich of them to use
            'sex': True,
            'education': True,
            'economy': True,
            'FSL': True,
            'RAW_1': True,
            'RAW_2': True,
            'RAW_3': True,
            'T88': True,
            'CustomParams': True

        }
        self.ParamsDrop = None
        self.valid_params = self.trainParam.copy()

    def setParam(self, key, val):
        try:
            if key not in self.valid_params:
                print(f'Param {key} does not exist')
                raise Exception()
            self.trainParam[key] = val
        except Exception as error:
            print('Param does not exist')
            print('Resetting to default value')

    def read_params_from_file_and_set(self, file_path):
        print(
            f"Read parameters dictionary at relative location {file_path} and setting them ")

        with open(file_path, 'r') as file:
            for line in file:
                # Strip leading and trailing whitespace
                line = line.strip()
                # Skip lines that are empty or start with #
                if not line or line.startswith('#'):
                    continue
                line = line.strip()
                if '#' in line:
                    line = line.split('#', 1)[0].strip()
                    # Skip line if only comment remains after stripping
                    if not line:
                        continue

                # print(line)
                key, value = line.strip().split(':')
                # Convert value to the appropriate type
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and '.' in value:
                    value = float(value)
                self.setParam(key, value)

    def write_dict_to_file(self, file_path):

        with open(file_path, 'w') as file:
            for key, value in self.trainParam.items():
                file.write(f'{key}:{value}\n')
        print(f"wrote parameters dictionary at relative location {file_path}")

    def create_params_file(self):
       
        paramsdrop = []
        paramsdrop.append(['ID', 'CDR','MMSE', 'Delay', 'USE', 'Hand','Dementia'])

        if self.trainParam['use_identifying_data'] == 'False':
            print('lala')
            paramsdrop.append(['Age', 'M/F', 'Educ', 'SES'])
        else:
            if self.trainParam['age'] == 'False':
                paramsdrop.append('Age')
            if self.trainParam['sex'] == 'False':
                paramsdrop.append('M/F')
            if self.trainParam['education'] == 'False':
                paramsdrop.append('Educ')
            if self.trainParam['economy'] == 'False':
                paramsdrop.append('SES')
        if self.trainParam['use_mri_data'] == 'False':
            paramsdrop.append(['PRED_FSL', 'PRED_RAW_1',
                              'PRED_RAW_2', 'PRED_RAW_3', 'PRED_T88'])
        else:
            if self.trainParam['FSL'] == 'False':
                paramsdrop.append('PRED_FSL')
            if self.trainParam['T88'] == 'False':
                paramsdrop.append('PRED_T88')
            if self.trainParam['RAW_1'] == 'False':
                paramsdrop.append['PRED_RAW_1']
            if self.trainParam['RAW_2'] == 'False':
                paramsdrop.append('PRED_RAW_2')
            if self.trainParam['RAW_3'] == 'False':
                paramsdrop.append('PRED_RAW_3')

        if self.trainParam['use_brain_size_data'] == 'False':
            paramsdrop.append(['eTIV', 'ASF', 'nWBV'])
        if 'True' in self.trainParam['CustomParams']:
            user_inputs = []
            possible_inputs = ['ID', 'SES', 'CDR', 'Delay', 'USE', 'Hand', 'Age',
                               'M/F', 'MMSE', 'eTIV', 'ASF', 'nWBV', 'Educ', 'PRED_FSL', 'PRED_RAW_1', 'PRED_RAW_2', 'PRED_RAW_3', 'PRED_T88']
            while True:
                print('Possible inputs:')
                print(possible_inputs)
                user_input = input(
                    "Write params to drop (type 'exit' to stop): ")

                # Check if the input is 'exit'
                if user_input.lower() == 'exit':
                    break
                # Take input from the user
                if user_input in possible_inputs:
                    # Add the input to the list of user inputs
                    user_inputs.append(user_input)
                    # Remove the input from the list of possible inputs
                    possible_inputs.remove(user_input)
                else:
                    print("Input not in the list of possible inputs. Try again.")
                # Add the input to the list
                user_inputs.append(user_input)
            paramsdrop = user_inputs
        return paramsdrop

    def separate_data(self):
        self.source_df['M/F'] = self.source_df['M/F'].map({'F': 1, 'M': 0})
        df_train = self.source_df[self.source_df['USE'] == 'T']
        df_test = self.source_df[self.source_df['USE'] != 'T']

        self.ParamsDrop = self.create_params_file()

        X_train = dropparameters(df_train, self.ParamsDrop)
        X_test = dropparameters(df_test, self.ParamsDrop)
        
        y_train = df_train['Dementia']
        y_test = df_test['Dementia']
        return X_train, X_test, y_train, y_test

    def trainandtest(self):

        X_train, X_test, y_train, y_test = self.separate_data()
        if self.trainParam['optimize'] == 'True':
            param_dist = {'n_estimators': np.arange(60, self.trainParam['estimators'], 20,dtype= int),
                          'max_depth': np.arange(2, self.trainParam['max_depth'])}
            print(param_dist)
            rf = RandomForestClassifier()
            rand_search = RandomizedSearchCV(rf,
                                             param_distributions=param_dist,
                                             n_iter=5,
                                             cv=5)
            rand_search.fit(X_train, y_train)
            print('Best hyperparameters:',  rand_search.best_params_)
            clf = rand_search.best_estimator_
        else:
            clf = RandomForestClassifier(
                n_estimators=self.trainParam['estimators'], max_depth=self.trainParam['max_depth'], criterion=self.trainParam['criterion'])
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        fn = X_train.columns
        if self.trainParam['plot'] == 'True':
            for i in range(3):
                fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=600)
                tree.plot_tree(clf.estimators_[i],
                               feature_names=fn,
                               class_names=['healthy', 'demented'],
                               filled=True,
                               impurity=True
                               )
                fig.savefig(f'plots/plottreefncn{i}.png')
                plt.figure()
            cm = confusion_matrix(y_test, y_pred)
            ConfusionMatrixDisplay(confusion_matrix=cm).plot()
            plt.savefig('plots/forest_confusion_matrix')
            plt.show()
            # Create a series containing feature importances from the model and feature names from the training data
            feature_importances = pd.Series(
                clf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
            # Plot a simple bar chart
            feature_importances.plot.bar(color="royalblue")
            plt.savefig('plots/feature_importance',bbox_inches='tight')
            plt.show()

        accuracy = accuracy_score(y_test, y_pred)

        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
         