import random
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold

from sklearn.metrics import average_precision_score
from sklearn.metrics import make_scorer
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# For Reproducibility
SEED = 88
random.seed(SEED)
np.random.seed(SEED)
np.random.RandomState(SEED);


def roc_auc(y_true, probs_pred):
    """ Calculate ROC area under curve """
    return roc_auc_score(y_true, probs_pred)


def pr_auc(y_true, probs_pred):
    """Calculate precision-recall area under curve"""
    # calculate area under curve
    return average_precision_score(y_true, probs_pred)


def evaluate_model(model, x, y):
    """ Evaluate the model using KFold """
    scoring = {'accuracy': make_scorer(accuracy_score),
               'f1': make_scorer(f1_score),
               'roc_auc': make_scorer(roc_auc, needs_proba=True),
               'pr_auc': make_scorer(pr_auc, needs_proba=True)
               }

    cv = KFold(n_splits=10, shuffle=True, random_state=SEED)
    scores = cross_validate(model, x, y, cv=cv,
                            scoring=scoring,
                            n_jobs=-1,
                            verbose=0)

    return scores


def display_scores(scores, metric):
    """ Display the avg and std score of the model"""
    print('='*60)
    for m in metric:
        name = 'test_'+m.lower()
        print(f"Metric: {m:>10} {'|':>5} Mean: {scores[name].mean():.3f} (+/- {scores[name].std()*2:.2f})")

