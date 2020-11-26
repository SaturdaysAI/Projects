#!/usr/bin/env python
# coding: utf-8

# In[161]:


import requests
import json
import time
import pandas as pd
import json
from time import sleep


# # Extracción de place id

# In[19]:


def place_id_extraction(place_name, api_key):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    
    params = {
    'input': place_name,
    'inputtype': 'textquery',
    'key': api_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    return results


# # Extracción de place details

# In[147]:


def place_details(place_id, api_key):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key
    }
    res = requests.get(endpoint_url, params = params)
    results =  json.loads(res.content)
    
    return results

