#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import numpy as np

import os
import os.path
import shutil


# # Leer datos

# In[2]:


#Subir un directorio
os.chdir("..")


# In[3]:


#Abrir json
json_df = pd.read_json('data/places_details.json')


# In[4]:


# Quedarnos con la columna que nos interesa
place_details = json_df['result']


# In[5]:


# concertir en lista
places_list = []
for i in place_details:
    place_dict = dict(i)
    places_list.append(place_dict)


# # Crear tabla

# In[11]:


df = pd.DataFrame()

for i in range(0, len(places_list)):
    temp_row = []
    try: 
        business_status = places_list[i]['business_status']
    except:
        business_status = ''
    try:    
        formatted_address = places_list[i]['formatted_address']
    except:
        formatted_address = ''
    try:
        formatted_phone_number = places_list[i]['formatted_phone_number']
    except:
        formatted_phone_number = ''
    try:
        latitude = places_list[i]['geometry']['location']['lat']
    except:
        latitude = ''
    try:
        longitude = places_list[i]['geometry']['location']['lng']
    except:
        longitude = ''
    try:
        name = places_list[i]['name']
    except:
        name = ''
    try:
        place_id = places_list[i]['place_id']
    except:
        place_id = ''
    try:
        rating = places_list[i]['rating']
    except:
        rating = ''
    try:
        user_ratings_total = places_list[i]['user_ratings_total']
    except:
        user_ratings_total = ''
    try:
        types = places_list[i]['types']
    except:
        types = ''    
    try:
        website = places_list[i]['website'] 
    except:
        website = ''
    try:
        price_level = places_list[i]['price_level']      
    except:
        price_level = float('nan')
    try:
        opening_hours = places_list[i]['opening_hours']['periods']  
    except:
        opening_hours = ''
    try:
        photos = places_list[i]['photos']
    except:
        photos = ''
    try:
        reviews = places_list[i]['reviews']
    except:
        reviews = ''

    temp_row.append(business_status)
    temp_row.append(formatted_address)
    temp_row.append(formatted_phone_number)
    temp_row.append(latitude)
    temp_row.append(longitude)
    temp_row.append(name)
    temp_row.append(place_id)
    temp_row.append(rating)
    temp_row.append(user_ratings_total)
    temp_row.append(website)
    temp_row.append(types)
    temp_row.append(price_level)
    temp_row.append(opening_hours)
    temp_row.append(photos)
    temp_row.append(reviews)
    
    df_temp = pd.DataFrame([temp_row], columns=['business_status', 'formatted_address', 'formatted_address',
                                                'latitude', 'longitude', 'name', 'place_id',
                                                'rating', 'user_ratings_total', 'website', 
                                                'types', 'price_level', 'opening_hours',
                                                'photos', 'reviews'
                                               ])
    df = pd.concat([df, df_temp])


# # Guardar datos

# In[14]:


df.to_csv('data/places_details_table.csv', index=False)


# In[ ]:




