#!/usr/bin/env python
# coding: utf-8

# In[10]:


import ssl
import sys
import paho.mqtt.client


# In[11]:


IP = '127.0.0.1'
PORT = 1884


# In[12]:


import ssl
import sys
 
import paho.mqtt.client
 
def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='casa/cocina/nevera', qos=2)

def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)

def main():
    client = paho.mqtt.client.Client(client_id='WATCHDOG', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host=IP, port=PORT)
    client.loop_forever()

if __name__ == '__main__':
    main()
    
sys.exit(0)


# In[ ]:




