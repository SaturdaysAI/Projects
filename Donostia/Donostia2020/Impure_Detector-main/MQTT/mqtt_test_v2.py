#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ssl
import sys
import paho.mqtt.client as mqtt 
import time


# In[2]:


IP = '127.0.0.1'
PORT = 1884
ID = 'WATCHer'
TOPIC_PUBLISH = 'dev/img'
TOPIC_SUSCRIBE = 'dev/img'


# In[ ]:


import ssl
import sys
 
import paho.mqtt.client
 
def on_connect(client, userdata, flags, rc):
    print(f'connected ID: {client._client_id}')
    client.subscribe(topic=TOPIC_SUSCRIBE, qos=2)

def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)

def on_publish(client, userdata, mid):
    pass
    # Wait for user to input a message
#    message = 'teta'
 #   if message:
  #      client.publish(TOPIC, message)
  #      sleep(.300)
#     client.disconnect()
    
    
def main():
    client = mqtt.Client(client_id= ID, clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(host=IP, port=PORT)
    client.loop_forever()
    
if __name__ == '__main__':
    main()
    
sys.exit(0)


# In[ ]:


f=open("b.jpg", "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)
client.publish("image",byteArr,0)

client.loop_forever()


# In[ ]:




