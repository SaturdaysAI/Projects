#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests
import pandas as pd
from time import sleep


# # Extracción

# In[5]:


def reviews_extraction(place_id:str, offset: int, api_key:str):
    endpoint_url = "https://wextractor.com/api/v1/reviews"
    
    params = {
        'auth_token': api_key,
        'id': place_id,
        'offset': offset,
        'sort': 'recency'
    }
    res = requests.get(endpoint_url, params = params)
    #Petición
    results =  json.loads(res.content)
    
    #Crear DataFrame
    df_temp = pd.DataFrame(results['reviews'])
    df_temp['place_id'] = place_id
    
    return df_temp

