#!/usr/bin/env python
# coding: utf-8

# # MODULES

import ssl
import sys
import paho.mqtt.client as mqtt 
import time
import csv
import os
import json
from datetime import datetime
import datetime as dtbug


# ### VARIOUS

# In[2]:


today = dtbug.date.today()
file_id = str(today) +'-VIOLATIONS.csv'
folder = './violations'
fields = {'index', 'img_id', 'time', 'Cx', 'Cy','Cz','temp','humidity'}

ANALYSIS = {'FILENAME': file_id, 'FOLDER' : folder, 
            'HEADERS': fields}

# work with several extensions
csv_file = os.path.join(ANALYSIS['FOLDER'], ANALYSIS['FILENAME'])
ANALYSIS['CSV'] = csv_file

###########################
if not os.path.exists(ANALYSIS['FOLDER']):
    os.makedirs(ANALYSIS['FOLDER'])
else:
    print('Path exists')
###########################


# ### DATA ANALYSIS

# writing to csv file  
with open(ANALYSIS['CSV'], 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(ANALYSIS['HEADERS'])  


def append_dict_as_row(file_name, data, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = csv.DictWriter(write_obj, 
                                     fieldnames=field_names,
                                    extrasaction='ignore',
                                    restval = 0)
        # Add dictionary as word in the csv
        dict_writer.writerow(data)


# ### PARAMETERS

BROKER_ADDRESS = '192.168.1.59'
PORT = 1884
ID = 'WATCHlisten'
TOPIC_SUBSCRIBE = ['IMG', 'DATA']


topics_vector = [(TOPIC_SUBSCRIBE[0], 0), (TOPIC_SUBSCRIBE[1], 0)]

def on_connect(client, userdata, flags, rc):
    print(f'connected ID: {client._client_id}')
    client.subscribe(topic=topics_vector, qos=2)
#     FLAG = True if !FLAG else FLAG = False
    
def on_message(client, userdata, message):
    global ANALYSIS, data
    
    if(message.topic == 'DATA'):
        bytedata=str(message.payload.decode("utf-8","ignore"))
        data=json.loads(bytedata)
        data['TIME'] = datetime.now().strftime('%H:%M:%S')
        data['DATE'] = datetime.now().strftime('%Y-%m-%d')
        print(data)
        append_dict_as_row(ANALYSIS['CSV'], data, ANALYSIS['HEADERS'])
    if(message.topic == 'IMG'):
        #Create a file with write byte permission
        f = open('./violations/' + data['DATE']+'x'+ str(data['img_id']) + '.jpg', "wb") #str(img_id)
        f.write(message.payload)
        f.close()
        print("Img Rcv")

def on_publish(client, userdata, mid):
    client.disconnect()

    
FLAG = False   
# configuration:
client = mqtt.Client(client_id= ID, clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_ADDRESS, PORT, keepalive=60)


# # MAIN

while True:
    client.loop_forever()

