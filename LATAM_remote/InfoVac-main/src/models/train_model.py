import os
import pandas as pd
import joblib

from src.models.support_functions import NormalizeTextTransformer
from datetime import datetime
import nltk
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer

from src.models.support_metrics import display_scores, evaluate_model, roc_auc, pr_auc, SEED


def load_data():

    if os.path.exists('../../data/train/X_train.csv'):
        X_train = pd.read_csv('../../data/train/X_train.csv')
        X_val = pd.read_csv('../../data/train/X_val.csv')
        X_test = pd.read_csv('../../data/train/X_test.csv')
        y_train = pd.read_csv('../../data/train/y_train.csv')
        y_val = pd.read_csv('../../data/train/y_val.csv')
        y_test = pd.read_csv('../../data/train/y_test.csv')

        return X_train, X_val, X_test, y_train, y_val, y_test

    else:
        file = '../../data/processed/covid_fakenews_es_utf_21_Oct_2020_17_29.csv'
        df = pd.read_csv(file)
        df['categoria'] = df['categoria'].map({'confiable': 1, 'no confiable': 0})
        df = shuffle(df, random_state=SEED)
        df.reset_index(drop=True, inplace=True)
        X = df['texto']
        y = df['categoria']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=SEED)

        X_train.to_csv('../../data/train/X_train.csv', index=False)
        X_val.to_csv('../../data/train/X_val.csv', index=False)
        X_test.to_csv('../../data/train/X_test.csv', index=False)

        y_train.to_csv('../../data/train/y_train.csv', index=False)
        y_val.to_csv('../../data/train/y_val.csv', index=False)
        y_test.to_csv('../../data/train/y_test.csv', index=False)

        return X_train, X_val, X_test, y_train, y_val, y_test


def train(config):
    X_train, X_val, X_test, y_train, y_val, y_test = load_data()

    # build the pipeline
    steps = [
        ('normalize', NormalizeTextTransformer(rm_sw=config.get('rm_sw'),
                                          rm_symb=config.get('rm_symb'),
                                          lemmatize=config.get('lemmatize'))),
        ('vectorize', TfidfVectorizer(lowercase=False, analyzer='word',
                                 ngram_range=config.get('ngram_range'),
                                 max_df=1.0, use_idf=True)),
        ('clf', SVC(C=config.get('C'), gamma=config.get('gamma'),
                    kernel=config.get('kernel'), random_state=SEED,
                    probability=True))
    ]

    model_pipe = Pipeline(steps=steps, verbose=1)

    # # Validate
    scores = evaluate_model(model_pipe, x=X_train, y=y_train)
    print('Validation: Train dataset')
    display_scores(scores, metric=['accuracy', 'f1', 'roc_auc', 'pr_auc'])

    # Final evaluation with test set
    model_pipe.fit(X=X_train, y=y_train)
    y_pred = model_pipe.predict(X_test)
    y_prob = model_pipe.predict_proba(X_test)
    print('\n')
    print('Validation: Test dataset')
    print('=' * 20)
    print(f'Accuracy:', accuracy_score(y_test, y_pred))
    print(f'F1-Score:', f1_score(y_test, y_pred))
    print(f'ROC-AUC:', roc_auc(y_test, y_prob[:, 1]))
    print(f'PR-AUC:', pr_auc(y_test, y_prob[:, 1]))

    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save the model
    c_day = datetime.now().strftime('%d_%h_%Y_%H_%M')
    joblib.dump(model_pipe, f'../../models/svm_pipeline_{c_day}.sav')


if __name__ == '__main__':
    nltk.download('stopwords')
    config = {
        "rm_sw": True,  # No stopwords
        "rm_symb": True,  # Remove numbers, special characters, accents
        "lemmatize": True,  # Lemmatize the words
        "ngram_range": (1, 1),  # Windows
        'features': 'texto',  # Column used as the input feature
        'random_state': SEED,  # To reproducibility
        'kfolds': 10,  # Amount of folds for evaluation
        'C': 13.126,
        'gamma': 0.6121,
        'kernel': 'rbf'
    }
    train(config)
