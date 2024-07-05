# Sobre el Modelo

## Evaluación

Tras ejecutar el script `scripts/evaluate.py`, obtenemos los siguientes valores:

### Test Loss: 0.9252066016197205

#### ¿Qué significa? 
La pérdida (loss) es una medida de qué que representa el error del modelo en la tarea de predicción.

#### Cómo se interpreta: 
Un valor de pérdida más bajo generalmente indica un mejor rendimiento del modelo, ya que significa que el error es menor. 

#### Importancia: 
La pérdida es utilizada durante el entrenamiento para ajustar los parámetros del modelo y reducir el error. En la fase de evaluación, ayuda a entender qué tan bien está funcionando el modelo con datos nuevos que no ha visto antes (datos de prueba).

### Test Accuracy: (83.26%) 0.8325544595718384

#### ¿Qué significa? 
La precisión es la proporción de predicciones correctas que hace el modelo en comparación con el total de predicciones. Es una medida de cuán a menudo el modelo acierta.

#### Cómo se interpreta: 
En este caso, una precisión del 83.26% significa que, de cada 100 predicciones que hace el modelo, aproximadamente 83 son correctas. Esto es una indicación de que el modelo está funcionando bastante bien, ya que acierta la mayoría de las veces.

#### Importancia: 
La precisión es una métrica importante para entender la efectividad del modelo, especialmente en problemas de clasificación. 