import pandas as pd
import numpy as np
import wfdb
import ast


def load_raw_data(df, sampling_rate, path):
    """
    Loads raw ECG data from the specified files and returns it as a numpy array.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the filenames of the ECG records.
    sampling_rate (int): The sampling rate of the ECG data. If 100, low-resolution data is loaded; otherwise, high-resolution data is loaded.
    path (str): The path to the directory containing the ECG data files.

    Returns:
    numpy.ndarray: A numpy array containing the loaded ECG signals.

    Example:
    df = pd.read_csv('ptbxl_database.csv')
    data = load_raw_data(df, 100, '/path/to/data/')
    """
    if sampling_rate == 100:
        data = [wfdb.rdsamp(path + f) for f in df.filename_lr]
    else:
        data = [wfdb.rdsamp(path + f) for f in df.filename_hr]
    data = np.array([signal for signal, meta in data])
    return data


def aggregate_diagnostic(y_dic, agg_df):
    """
    Aggregates diagnostic information from the provided diagnostic codes using the aggregation DataFrame.

    Parameters:
    y_dic (dict): A dictionary of diagnostic codes for a single ECG record.
    agg_df (pandas.DataFrame): DataFrame containing diagnostic aggregation information.

    Returns:
    list: A list of aggregated diagnostic classes for the provided diagnostic codes.

    Example:
    agg_df = pd.read_csv('scp_statements.csv', index_col=0)
    y_dic = {'NORM': 1, 'MI': 2}
    aggregated = aggregate_diagnostic(y_dic, agg_df)
    """
    tmp = []
    for key in y_dic.keys():
        if key in agg_df.index:
            tmp.append(agg_df.loc[key].diagnostic_class)
    return list(set(tmp))


def find_max_condition(condition_dict):
    if isinstance(condition_dict, dict):
        max_condition = max(
            condition_dict, key=condition_dict.get
        )  # Find the key with the maximum value
        return {max_condition: condition_dict[max_condition]}
    else:
        return None


def filter_by_confidence(dataframe, column_name, threshold=50.0):
    """
    Filters the DataFrame to only include rows where the highest diagnostic confidence is above a specified threshold.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame containing the rows to filter.
    column_name (str): The column name where each entry is a tuple containing the diagnostic condition and its score.
    threshold (float, optional): The confidence threshold for keeping rows. Defaults to 50.0.

    Returns:
    pd.DataFrame: A DataFrame filtered to only include rows with diagnostic confidence above the threshold.

    filtered_df = filter_by_confidence(df, 'Highest_Score_Condition', 50)
    """
    # Filter rows based on the second element in the tuple (score) being above the threshold
    filtered_df = dataframe[
        dataframe[column_name].apply(lambda x: x[1] >= threshold if x else False)
    ]

    return filtered_df


def load_data_from_directory(path_to_directory, sampling_rate):
    """
    Loads patient data, ECG data, and performs diagnostic aggregation.

    Parameters:
    path_to_directory (str): The path to the directory containing the data files.
    sampling_rate (int): The sampling rate of the ECG data.

    Returns:
    tuple: A tuple containing:
        - numpy.ndarray: A numpy array containing the loaded ECG signals.
        - pandas.DataFrame: DataFrame containing patient and diagnostic data.
        - pandas.DataFrame: DataFrame containing diagnostic aggregation information.

    Example:
    path = '/path/to/data/'
    sampling_rate = 100
    X, Y, agg_df = load_data_from_directory(path, sampling_rate)
    """
    # Load and convert annotation data
    Y = pd.read_csv(path_to_directory + "ptbxl_database.csv", index_col="ecg_id")
    Y.scp_codes = Y.scp_codes.apply(lambda x: ast.literal_eval(x))

    # No removal of duplicate records as it is a second observation
    # Y.drop_duplicates(["patient_id"])

    # Select highest confidence condition for each record
    Y["scp_codes"] = Y["scp_codes"].apply(find_max_condition)

    threshold = 70
    Y.to_csv("test.csv")
    # Filter the DataFrame to drop rows where the max value is less than the threshold
    Y = Y[Y["scp_codes"].apply(lambda x: list(x.values())[0] if x else 0) >= threshold]

    # Load raw signal data
    X = load_raw_data(Y, sampling_rate, path_to_directory)

    # Load scp_statements.csv for diagnostic aggregation
    agg_df = pd.read_csv(path_to_directory + "scp_statements.csv", index_col=0)
    agg_df = agg_df[agg_df.diagnostic == 1]

    Y["diagnostic_superclass"] = Y.scp_codes.apply(
        lambda x: aggregate_diagnostic(x, agg_df)
    )

    return X, Y, agg_df


# function to do all data cleaning and create new column 'diagnostic_binary' and save the cleaned data to the folder data
def preprocess_data(X, Y):
    """
    Preprocess the data by removing samples with missing values in the diagnostic superclass categories and creating a new column 'diagnostic_binary'.
    """
    # create new column for the superclass aggregation in 2 classes 'MI' and 'NORMAL'
    Y["diagnostic_binary"] = Y["diagnostic_superclass"].apply(
        lambda x: "MI" if "MI" in x else "NORMAL"
    )

    # drop the rows with missing values in the labels 'diagnostic_superclass'
    Y_clean = Y[Y["diagnostic_superclass"].apply(lambda x: len(x)) > 0]

    # drop columns that are not needed
    # Y_clean = Y_clean.drop(['diagnostic_superclass'], axis=1)

    # save the cleaned data to the folder data
    Y_clean.to_csv("data/Y_clean.csv", index=False)
    np.save("data/X.npy", X)

    return X, Y_clean


def get_train_test_split(X, Y_clean, test_fold=10, validation=False):
    """
    Splits the data into training, test, and optionally validation sets based on the stratification fold.

    Parameters:
    X (numpy.ndarray): The ECG signal data.
    Y (pandas.DataFrame): DataFrame containing patient and diagnostic data.
    test_fold (int, optional): The fold number to use for the test set. Defaults to 10.
    validation (bool, optional): Whether to include a validation set. Defaults to False.

    Returns:
    tuple: A tuple containing:
        - numpy.ndarray: Training set ECG signals.
        - numpy.ndarray: Test set ECG signals.
        - pandas.Series: Training set diagnostic classes.
        - pandas.Series: Test set diagnostic classes.
        - numpy.ndarray (optional): Validation set ECG signals.
        - pandas.Series (optional): Validation set diagnostic classes.

    Example:
    X_train, X_test, y_train, y_test = get_train_test_split(X, Y, test_fold=10)
    """
    validation_folds = [8, 9]
    # From the documentation of the dataset, they recommend for the test fold to be 10 and 8 and 9 as validation.

    X_train = X[
        np.where(
            (Y_clean.strat_fold != test_fold)
            & (~Y_clean.strat_fold.isin(validation_folds))
        )
    ]
    y_train = Y_clean[
        (Y_clean.strat_fold != test_fold) & (~Y_clean.strat_fold.isin(validation_folds))
    ].diagnostic_binary

    X_test = X[np.where(Y_clean.strat_fold == test_fold)]
    y_test = Y_clean[Y_clean.strat_fold == test_fold].diagnostic_binary

    if validation:
        X_val = X[np.where(Y_clean.strat_fold.isin(validation_folds))]
        y_val = Y_clean[Y_clean.strat_fold.isin(validation_folds)].diagnostic_binary

        return X_train, X_test, y_train, y_test, X_val, y_val
    else:
        return X_train, X_test, y_train, y_test