import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier 
import joblib
# Read data into pandas dataframe
df=pd.read_csv('app\df_to_ml.csv')
#Define Feature Matrix (X) and Label Array (y)
X=df.drop(['investment'],axis=1)
y=df['investment']
lr = DecisionTreeClassifier(random_state=3838, max_depth=4)
lr.fit(X,y)

#Serialize the model and save
joblib.dump(lr, 'app\dt4.pkl')
print("dt4 Model Saved")
#Load the model
lr = joblib.load('app\dt4.pkl')
# Save features from training
rnd_columns = list(X.columns)
joblib.dump(rnd_columns, 'app\dt4_columns.pkl')
print("dt4 Model Colums Saved")