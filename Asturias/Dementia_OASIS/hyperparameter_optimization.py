# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:13:37 2024

@author: Pablo
"""
import os
import torch
import pandas as pd
import numpy as np
import torchvision
import torch.optim as optim

import optuna
from optuna.visualization import plot_optimization_history, plot_param_importances, plot_parallel_coordinate, plot_slice
from optuna.storages import JournalStorage, JournalFileStorage

from matplotlib import pyplot as plt

from torch import nn
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, f1_score
from sklearn.preprocessing import MinMaxScaler
import itertools
import time

from misc_aux import getDataFrameFromDict, Logger, parse_hyperconstraints_line, load_hyperparameters_constraints_from_file
from custom_dataset import CustomTransform, CustomDataset, getDatasetIDS
from pickle_aux import compressed_pickle, decompress_pickle, pet_save



def get_optimal_params(df_results):

    scaler = MinMaxScaler()
    df_results[['accuracy', 'precision', 'recall', 'f1']] = scaler.fit_transform(
        df_results[['accuracy', 'precision', 'recall', 'f1']])
    df_results['average_loss'] = 1 - \
        scaler.fit_transform(df_results[['average_loss']])

    def combined_metric(row, alpha, beta, gamma):
        return (alpha * row['accuracy'] +
                beta * row['precision'] +
                gamma * row['recall'])

    # Define the objective function for Optuna
    def objective(trial):
        alpha = trial.suggest_float('alpha', 0.0, 1.0)
        beta = trial.suggest_float('beta', 0.0, 1.0)
        gamma = trial.suggest_float('gamma', 0.0, 1.0)
        
        # Normalize the sum of weights to 1
        total_weight = alpha + beta + gamma
        alpha /= total_weight
        beta /= total_weight
        gamma /= total_weight

        # Apply the combined metric function to the DataFrame
        df_results['combined_score'] = df_results.apply(
            lambda row: combined_metric(row, alpha, beta, gamma), axis=1)

        # Find the highest combined score
        # best_model_idx = df_results['combined_score'].idxmax()
        # best_combined_score = df_results.loc[best_model_idx, 'combined_score']

        best_combined_score = df_results['combined_score'].max()

        # Return the negative of the best combined score because Optuna minimizes the objective function
        return best_combined_score

    # Run the Optuna study
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)

    # Get the best parameters
    best_params = study.best_params
    print("Best parameters:", best_params)

    # Use the best parameters to find the best model
    alpha, beta, gamma = best_params['alpha'], best_params[
        'beta'], best_params['gamma']
    total_weight = alpha + beta + gamma 
    alpha /= total_weight
    beta /= total_weight
    gamma /= total_weight
    

    df_results['combined_score'] = df_results.apply(
        lambda row: combined_metric(row, alpha, beta, gamma), axis=1)

    df_results['rank'] = df_results['combined_score'].rank(ascending=False)

    df_results.sort_values(by='rank')

    return df_results


def generate_variations(base_params, param_ranges):
    keys, values = zip(*param_ranges.items())
    variations = [dict(zip(keys, v)) for v in itertools.product(*values)]
    varied_params = []

    for variation in variations:
        params = base_params.copy()
        params.update(variation)
        varied_params.append(params)
    print("number of variations", len(varied_params))
    return varied_params


def get_all_parameter_files(directory, process_files=[],hyper = False):
    #if not hyper:
        return [os.path.join(directory, f) for f in os.listdir(directory) if (f.endswith(".txt") and 'output' not in f and 'skip' not in f) and (os.path.splitext(os.path.basename(f))[0] in process_files)]
    #else:
    #    return [os.path.join(directory, f) for f in os.listdir(directory) if (f.endswith(".txt") and 'output' not in f and 'skip' not in f and 'hyper' in f) and (os.path.splitext(os.path.basename(f))[0] in process_files)]

def read_config(file_name):
    config_dict = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.split('#')[0].strip()  # Remove comments and whitespace
            if line and ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                if value.isdigit():
                    config_dict[key] = int(value)
                elif value.replace('.', '', 1).isdigit() and '.' in value:
                    config_dict[key] = float(value)
                else:
                    config_dict[key] = value
                # print(line)
    print('file read', config_dict)
    return config_dict

def parsehyperparams(trial, hyperparams, baseparams):
    # loads an hyperparameters file and updatesa base params dictionary with optunas trial.suggest_
    for key, value in hyperparams.items():
       low_value, high_value, step, extraparam = value
       
       # If the extraparam is not provided, treat it as a string
       if extraparam == None:
           if isinstance(low_value, int) and isinstance(high_value, int):
               suggested_value = trial.suggest_int(key, low_value, high_value, step=step)
           elif isinstance(low_value, float) and isinstance(high_value, float):
               suggested_value = trial.suggest_float(key, low_value, high_value, step=step)
           else:
               suggested_value = trial.suggest_categorical(key, [str(low_value), str(high_value)])
           
           
       elif 'log' in extraparam:
           if isinstance(low_value, int) and isinstance(high_value, int):
               suggested_value = trial.suggest_int(key, low_value, high_value, log = True)
           elif isinstance(low_value, float) and isinstance(high_value, float):
               suggested_value = trial.suggest_float(key, low_value, high_value, log = True)
           else:
               suggested_value = trial.suggest_categorical(key, [str(low_value), str(high_value)])
       # If extraparam is log, treat it as a categorical parameter
       
       # Update base_hyperparameters dictionary
       #print(key, suggested_value)
       baseparams[key] = suggested_value
    #baseparams['verbosity'] = 0
    return baseparams

def find_hyperparams_optuna(obj,base_folder_path,hyperparams_path,save_study_path,dataset_path, process_files, logpath=None, n_trials = 200, timeout = 30000): #8 horas max por material):
    
    files = get_all_parameter_files(hyperparams_path, process_files)
    hyperfiles = get_all_parameter_files(hyperparams_path, process_files, hyper = True)
    
    
    files = set(os.listdir(base_folder_path))
    hyperfiles =  set(os.listdir(hyperparams_path))
    availablefiles = get_all_parameter_files(base_folder_path, process_files)
    #print(files)
    #print(hyperfiles)
    #print(availablefiles)
    for file_name in files:
        filenamepath = os.path.join(base_folder_path,file_name)
        if filenamepath not in availablefiles:
            #print(filenamepath)
            #print(os.path.splitext(filenamepath)[0])
            continue
    # Generate the corresponding file name in folder2
        hyper_file_name = f"hyper_{file_name}"
        
        if hyper_file_name in hyperfiles:
            print(hyper_file_name)
            print(file_name)
            try:
                opt_hyperparamters = load_hyperparameters_constraints_from_file(os.path.join(hyperparams_path, hyper_file_name))
                #dict_config = read_config(os.path.join(hyperparams_path, file_name))
                obj.read_params_from_file_and_set(os.path.join(base_folder_path,file_name), printea = False)
                pet_save(obj,'tmp_nn.p')
            except:
                print("there is a problem inside the parameters files")
                
            file_basename = os.path.basename(file_name)
            file_without_extension = os.path.splitext(file_basename)[0]
            if logpath is not None:
                timeofcreation = time.strftime('%Y_%m_%d_%H_%M_%S')
                loggingpath = logpath + file_without_extension + "_" + timeofcreation + "_log.txt"

            logger = Logger(file_path=loggingpath)
            obj.logger = logger
            obj.read_params_from_file_and_set(os.path.join(base_folder_path,file_name), printea = False)
            obj.logger.verbosity = obj.trainParam['verbosity']
            obj.logger.verbosity = 0

            print(opt_hyperparamters)
            results = []
            
            def objective(trial):
                
                #back to defaults
                obj.read_params_from_file_and_set(os.path.join(base_folder_path,file_name), printea = False)
                obj.logger.verbosity = obj.trainParam['verbosity']
                obj.logger.verbosity = 0
                #now we change the params using and force them with trial.suggest
                config_dict = parsehyperparams(trial, opt_hyperparamters, obj.trainParam)
                obj.set_params_dict_to_object(config_dict, printea = False)
                print(obj.trainParam)
                obj.setTransform([CustomTransform()])
                loss = obj.train()
                labels, predicted, partial_results = obj.test()
                 

                return loss
            #sampler = optuna.samplers.CmaEsSampler()
            study_name=f'{file_without_extension}_hyperparameter_study'
            #storage_name = "sqlite:///{}.db".format(study_name)
            logname = os.path.join(save_study_path,f"{file_without_extension}-optuna-journal.log")
            lock_obj = optuna.storages.JournalFileOpenLock(logname)
            storage_name = JournalStorage(JournalFileStorage(logname, lock_obj = lock_obj))

            study = optuna.create_study(
                    study_name=study_name,
                    storage=storage_name,
                    direction="minimize",
                    load_if_exists=True
)
            
            #study = optuna.create_study(direction="minimize")  # 'minimize' because objective function is returning loss
            failedtrials = False
            failed = 0
            
            #fig = optuna.visualization.matplotlib.plot_timeline(study)
            for trial in study.trials:
                if trial.state == optuna.trial.TrialState.FAIL: 
                    study.enqueue_trial(trial.params)
                    failed += 1
                    failedtrials = True
            
            if failedtrials:
                print(f"now running {failed} trials that failed to finish before")
                remaining = n_trials - len(study.trials) + 1
                print(f"now running {remaining} trials that remained from before")
                study.optimize(objective,n_trials = remaining, timeout = timeout, show_progress_bar=True)
            else:
                study.optimize(objective, n_trials=n_trials, timeout = timeout, show_progress_bar=True)
            
            pruned_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]
            complete_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
            
            best_params = study.best_params
            print("Best parameters:", best_params)
            print("Study statistics: ")
            print("  Number of finished trials: ", len(study.trials))
            print("  Number of pruned trials: ", len(pruned_trials))
            print("  Number of complete trials: ", len(complete_trials))
            print("Best Trials", study.best_trials)
            print("Best trial:")
            trial = study.best_trial
            
            print("  Value: ", trial.value)
            
            print("  Params: ")
            for key, value in trial.params.items():
                print("    {}: {}".format(key, value))
            df_results = study.trials_dataframe(attrs=("number", "value", "params", "state"))
            
            df_results.to_csv('{0}.csv'.format(
                os.path.join(dataset_path,file_without_extension)), index=False)
            
            #now we save to a file for posterior analysis,
            compressed_pickle(study, os.path.join(save_study_path, file_without_extension))
            os.remove('tmp_nn.p')
            time.sleep(300)
            #os.remove(f"{file_without_extension}-optuna-journal.log")
        else:
            print(f"Matching file for {file_name} not found in folder2.")


def visualizeresults (study_path):
    file_basename = os.path.basename(study_path)
    file_basename = os.path.splitext(file_basename)[0]
    
    
    study = decompress_pickle(study_path)
    print("Best trial until now:")
    print(" Value: ", study.best_trial.value)
    print(" Params: ")
    for key, value in study.best_trial.params.items():
        print(f"    {key}: {value}")
        
    best_params = study.best_params
    print("Best parameters:", best_params)
    print("Study statistics: ")
    pruned_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]
    complete_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))
    print("Best Trials", study.best_trials)
    print("Best trial:")
    trial = study.best_trial
    
    print("  Value: ", trial.value)
    
    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))
        
        
    if not os.path.exists(f"plots/{file_basename}"):
        os.makedirs(f"plots/{file_basename}")
    optimization_history = optuna.visualization.matplotlib.plot_optimization_history(study)
    optimization_history.set_yscale('log')
    plt.savefig(f"plots/{file_basename}/optimization_history.jpg")
    plt.show()
    # Visualize parameter importances
    param_importances =  optuna.visualization.matplotlib.plot_param_importances(study)
    plt.savefig(f"plots/{file_basename}/param_importances.jpg")
    plt.show()
    
    # Visualize parallel coordinate plot
    parallel_coordinate =  optuna.visualization.matplotlib.plot_parallel_coordinate(study)
    plt.savefig(f"plots/{file_basename}/parallel_coordinate.jpg")
    plt.show()
    
    # Visualize slice plot
    slice_plot =  optuna.visualization.matplotlib.plot_slice(study)
    plt.savefig(f"plots/{file_basename}/sliceplot.jpg")
    plt.show()
    keys = list(trial.params.keys())
    print(len(trial.params))
    for i in range(len(trial.params)- 1):
        for j in range(i + 1, len(trial.params)):
            
            fig = optuna.visualization.matplotlib.plot_contour(study, params=[keys[i], keys[j]])
            plt.savefig(f"plots/{file_basename}/contour_{keys[i]}_{keys[j]}.jpg")
            plt.show()
    fig =  optuna.visualization.matplotlib.plot_contour(study )
    plt.savefig(f"plots/{file_basename}/plotcontour.jpg")
    plt.show()
    
    fig = optuna.visualization.matplotlib.plot_timeline(study)
    plt.savefig(f"plots/{file_basename}/timeline.jpg")
    plt.plot()