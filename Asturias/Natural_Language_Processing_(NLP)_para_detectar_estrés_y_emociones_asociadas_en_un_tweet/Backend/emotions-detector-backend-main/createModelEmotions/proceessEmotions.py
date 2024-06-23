# Data manipulation
import pandas as pd


import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
# Save models into a file!
import os
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from text_processingEmotions import clean_text


#disable CUDA no GPU computers
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

df=pd.read_csv('./text.csv')

labels = df["label"].values
textsToClean = df["text"].values

# Clean the text data
texts = [clean_text(text) for text in textsToClean]

outputs = []

inputs = tf.constant(texts)

#sadness (0), joy (1), love (2), anger (3), fear (4), and surprise (5)

for label in labels:

    arrayOfZeros= [0,0,0,0,0,0]
    arrayOfZeros[label]=1
    outputs.append(arrayOfZeros)

outputs = tf.constant(outputs)

split_index = int(0.8 * len(inputs))


train_data = []

#Crea un dataset de entrenamiento, incluye las frases (entradas) y las etiquetas (salidas)
train_data.append(inputs[:split_index])
train_data.append(outputs[:split_index])

#Crea un dataset de evaluación, incluye las frases (entradas) y las etiquetas (salidas).
evaluate_data = []
evaluate_data.append(inputs[split_index:])
evaluate_data.append(outputs[split_index:])


#Convert to NumPy arrays
train_texts, train_labels = tfds.as_numpy(train_data)

evaluate_texts, evaluate_labels = tfds.as_numpy(evaluate_data)


# text=>numbers
model_nnlm = "https://tfhub.dev/google/nnlm-en-dim50-with-normalization/2"
hub_layer = hub.KerasLayer(model_nnlm, input_shape=[], dtype=tf.string, trainable=True)

# ¿Que genera este modelo como output? 
print(hub_layer(train_texts[:1]))
# [0.05040912, -0.15988576, 0.2461916, 0.2332126, -0.3881552, 0.1005447, 0.22930293, 0.04687591, -0.27713916, -0.26926598, 0.04524967, 0.33750767, -0.04390128, -0.17454425, -0.09238187, -0.21451329, -0.0307375, 0.11426938, 0.10953096, -0.13111621, -0.17918059, -0.30201793, -0.01961316, -0.19642058, -0.33542755, -0.15204693, -0.13795857, 0.13474914, 0.1494579, 0.06782167, 0.09041105, -0.2536934, 0.04294463, 0.00060515, 0.01632698, -0.06662191, 0.30713016, 0.04084823, 0.46430537, -0.1918756, 0.27968672, -0.083872, -0.14772423, 0.23210736, -0.23955503, -0.23241633, -0.14805655, -0.1384443, 0.20030525, 0.18372603]

# Creamos nuestro propio modelo usando las "hub_layer", al inicio
model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(6, activation='sigmoid'))


# Compilamos el modelo
learning_rate = 0.001
optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer,
              loss=tf.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.metrics.BinaryAccuracy(threshold=0.2, name='accuracy')])

early_stopping = EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)


# Iniciamos el entrenamiento
history = model.fit(train_texts,
                    train_labels,
                    epochs=100,
                    batch_size=512,
                    validation_data=(evaluate_texts, evaluate_labels),
                    callbacks=[early_stopping],
                    verbose=1)

# Mostramos todos los pasos del history
print(history.history)

# Gráfica de la pérdida y precisión
plt.figure(figsize=(12, 6))

# Pérdida
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Precisión
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.show()


# Evaluamos el modelo
results = model.evaluate(evaluate_texts, evaluate_labels)
# Son perdida y precisión
#print(results)

model.save("emotionsModelWithCleanData2.keras")