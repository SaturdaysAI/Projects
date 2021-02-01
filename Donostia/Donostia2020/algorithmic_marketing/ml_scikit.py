import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, Normalizer
from sklearn.model_selection import train_test_split, learning_curve

class mlScikitClass:
    def __init__(self): 
        self.name = "Clase para Supervised ML"

    def regression(self, X_train, y_train, X_test, y_test, tipo):
        if tipo == 'linear':
            model = LinearRegression()
        elif tipo == 'Lasso-iter':
            model = Lasso(max_iter=1000000)
        elif tipo == 'Lasso':
            model = Lasso()
        else:
            model = Ridge()
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(tipo +" MAE: {}".format(mae))
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(tipo +" RMSE: {}".format(rmse))
        rsquare = model.score(X_test,y_test)
        print(tipo +" Accuracy (R-square) : {}".format(rsquare))
        
    def normalize(self, df, tipo):
        if tipo == 'Standard':
            transformer = Normalizer()
        elif tipo == 'MinMax':
            transformer = MinMaxScaler()
        elif tipo == 'Robust':
            transformer = RobustScaler()
        else:
            transformer = Normalizer()
        
        print('Datos transformados usando la técnia: '+ tipo)
        scaled = transformer.fit_transform(df)  
        scaled = pd.DataFrame(scaled)
        scaled.columns = df.columns
        return scaled
    
    def filtrar_outlier_tukey(self, x):
        q1 = np.percentile(x, 25)
        q3 = np.percentile(x, 75)
        iqr = q3 - q1 
        print("[q1=%f, q3=%f, iqr=%f]" % (q1, q3, iqr))
        
        floor = q1 - 1.5*iqr
        ceiling = q3 + 1.5*iqr
        print("[floor=%f, ceiling=%f]" % (floor, ceiling))
        
        outlier_indices = list(x.index[(x < floor)|(x > ceiling)])
        outlier_values = list(x[outlier_indices])
    
        return outlier_indices
        #return outlier_indices, outlier_values
        

    
    def validation_curves(self, model_params, metrics, df):
        
        def pooled_var(stds):
            # https://en.wikipedia.org/wiki/Pooled_variance#Pooled_standard_deviation
            n = 5 # size of each group
            return np.sqrt(sum((n-1)*(stds**2))/ len(stds)*(n-1))
        
        
        fig, axes = plt.subplots(1, len(model_params), 
                                 figsize = (5*len(model_params), 7),
                                 sharey='row')
    
        axes[0].set_ylabel("Score", fontsize=25)
    
        for idx, (param_name, param_range) in enumerate(model_params.items()):
            grouped_df = df.groupby(f'param_{param_name}')[metrics]\
                .agg({'mean_train_score': 'mean',
                      'mean_test_score': 'mean',
                      'std_train_score': pooled_var,
                      'std_test_score': pooled_var})
    
            axes[idx].set_xlabel(param_name, fontsize=30)
            axes[idx].set_ylim(0.0, 1.1)
            lw = 2
            axes[idx].plot(param_range, grouped_df['mean_train_score'], label="Training score",
                        color="darkorange", lw=lw)
            axes[idx].fill_between(param_range,grouped_df['mean_train_score'] - grouped_df['std_train_score'],
                            grouped_df['mean_train_score'] + grouped_df['std_train_score'], alpha=0.2,
                            color="darkorange", lw=lw)
            axes[idx].plot(param_range, grouped_df['mean_test_score'], label="Cross-validation score",
                        color="navy", lw=lw)
            axes[idx].fill_between(param_range, grouped_df['mean_test_score'] - grouped_df['std_test_score'],
                            grouped_df['mean_test_score'] + grouped_df['std_test_score'], alpha=0.2,
                            color="navy", lw=lw)
    
        handles, labels = axes[0].get_legend_handles_labels()
        fig.suptitle('Validation curves', fontsize=40)
        fig.legend(handles, labels, loc=8, ncol=2, fontsize=20)
    
        fig.subplots_adjust(bottom=0.25, top=0.85)  
        plt.show()
        
    def learning_curves(self, model, X, y, cv, scoring, n_jobs, array):
        # Create CV training and test scores for various training set sizes
        train_sizes, train_scores, test_scores = learning_curve(model, 
                                                                X, y,
                                                                # Number of folds in cross-validation
                                                                cv=cv,
                                                                # Evaluation metric
                                                                scoring=scoring,
                                                                # Use all computer cores
                                                                n_jobs=n_jobs, 
                                                                # 50 different sizes of the training set
                                                                train_sizes=array)
        
        # Create means and standard deviations of training set scores
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        
        # Create means and standard deviations of test set scores
        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)
        
        # Draw lines
        plt.plot(train_sizes, train_mean, '--', color="r",  label="Training score")
        plt.plot(train_sizes, test_mean, color="g", label="Cross-validation score")
        
        # Draw bands
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#DDDDDD")
        plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#DDDDDD")
        
        # Create plot
        plt.title("Learning Curve")
        plt.xlabel("Training Set Size"), plt.ylabel("Accuracy Score"), plt.legend(loc="best")
        plt.tight_layout()
        plt.show()
