from tensorflow.keras import models
model = models.load_model('../model/model_trained_3class.hdf5', compile=False)
with open('../model/model_summary.txt', 'w') as f:
    model.summary(print_fn=lambda x: f.write(x + '\n'))