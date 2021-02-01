#Install Libraries
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
application = Flask(__name__)
@application.route('/prediction', methods=['POST'])
#define function
def predict():
 if lr:
    try:
        json_ = request.json
        print(json_)
        query = pd.get_dummies(pd.DataFrame(json_))
        query = query.reindex(columns=dt4_columns, fill_value=0)
        predict = list(lr.predict(query))
        return jsonify({'prediction': str(predict)})
    except:
        return jsonify({'trace': traceback.format_exc()})
 else:
    print ('Model not good')
    return ('Model is not good')
if __name__ == '__main__':
    try:
        port = 12345
    except:
        port = 12345 
lr = joblib.load('app/dt4.pkl') 
print('Model loaded')
dt4_columns = joblib.load('app/dt4_columns.pkl') # Load “dt4_columns.pkl”
print('Model columns loaded')
application.run(port=port, debug=True)