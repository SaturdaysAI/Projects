import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


# Define Column Names
columns=["timeRelativeRef", "samplingTime", "epoch", "latitude","longitude","altitude","speed", 
            "satellites","accelerationX", "accelerationY", "accelerationZ", "roll", "pitch","yaw",
            "temperatur","humidity", "barometricPressure","light","PM1.0_CF1", "PM2.5_CF1", "PM10.0_CF1",
            "PM1.0_Auto", "PM2.5_Auto", "PM10.0_Auto","label"]

# Read all data
Bricked1 = pd.read_csv("Labeled Training data\Bricked road\DATA002.CSV", names=columns)
Bricked2 = pd.read_csv("Labeled Training data\Bricked road\DATA004.CSV", names=columns)

Manhole = pd.read_csv("Labeled Training data\Manhole\DATA004.CSV", names=columns)

Pothole1 = pd.read_csv("Labeled Training data\Pothole\DATA001.CSV", names=columns)
#Pothole2 = pd.read_csv("Labeled Training data\Pothole\DATA002.CSV", names=columns)
Pothole3 = pd.read_csv("Labeled Training data\Pothole\DATA003.CSV", names=columns)

RoadJoint1 = pd.read_csv("Labeled Training data\Road joint\DATA001.CSV", names=columns)
RoadJoint2 = pd.read_csv("Labeled Training data\Road joint\DATA003.CSV", names=columns)

StormBasin1 = pd.read_csv("Labeled Training data\Storm basin\DATA001.CSV", names=columns)
StormBasin2 = pd.read_csv("Labeled Training data\Storm basin\DATA002.CSV", names=columns)
StormBasin3 = pd.read_csv("Labeled Training data\Storm basin\DATA003.CSV", names=columns)


# add labels in all DataFrames

Bricked1['label'] = 'bricked'
Bricked2['label'] = 'bricked'

Manhole['label'] = 'manhole'

Pothole1['label'] = 'pothole'
#Pothole2['label'] = 'pothole'
Pothole3['label'] = 'pothole'

RoadJoint1['label'] = 'roadJoint'
RoadJoint2['label'] = 'roadJoint'

StormBasin1['label'] = 'stormBasin'
StormBasin2['label'] = 'stormBasin'
StormBasin3['label'] = 'stormBasin'

# combine all above DataFrames # add Pothole2 when fixed

data = pd.concat([Bricked1,Bricked2, 
                Manhole, 
                Pothole1,Pothole3, 
                RoadJoint1, RoadJoint2,
                StormBasin1,StormBasin2, StormBasin3 ])

# keep related columns
df = data[['timeRelativeRef', 'samplingTime','accelerationX', 'accelerationY',
       'accelerationZ', 'roll', 'pitch', 'yaw', 'label']]


# check labels 
df.label.value_counts()

bricked = df[df['label'] == "stormBasin"]
x = bricked.timeRelativeRef
y = bricked.accelerationZ
#figure(figsize=(12, 6), dpi=80)
plt.plot(x, y)
plt.show()

print("DOne")



