#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies and Setup
get_ipython().system('pip install gmaps')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os
import json
import time
# API keys
# OpenWeatherMap API Key
weather_api_key = "42fc9adc90ea2e2c2fdd3e059f13a8de"
# Google API Key
g_key = "AIzaSyAqKJpKDT8joFxSRi-hVSjmLrx1eHgTZc"


# In[15]:


#Bring in cities we used in first part
weather_data = pd.read_csv(r"output_data/cities1.csv")
weather_data


# In[16]:


# Configure gmaps
gmaps.configure(api_key=g_key)

# Store latitude and longitude in locations
locations = weather_data[["Lat", "Lng"]]

# Store Humidity in humidity
humidity = weather_data["Humidity"]
# Plot Heatmap
fig = gmaps.figure(center=(46.0, -5.0), zoom_level=2)
max_intensity = np.max(humidity)

# Create heat layer
heat_layer = gmaps.heatmap_layer(locations, weights = humidity, dissipating=False, max_intensity=100, point_radius=3)

# Add layer
fig.add_layer(heat_layer)

# Display figure
fig


# In[17]:


# Narrow down the cities with wind speed less than 10 mph, cloudiness equals to 0 and max temp between 60 and 70
narrowed_city_df = weather_data.loc[(weather_data["Wind Speed"] <= 10) & (weather_data["Cloudiness"] == 0) &                                    (weather_data["Max Temp"] >= 60) & (weather_data["Max Temp"] <= 70)].dropna()

narrowed_city_df


# In[18]:


# Create a hotel_df
hotel_df = narrowed_city_df.loc[:,["City","Country", "Lat", "Lng"]]

# Add a "Hotel Name" column to the DataFrame.
hotel_df["Hotel Name"] = hotel_df

# Display the result
hotel_df


# In[19]:


base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

params = {"type" : "hotel",
          "keyword" : "hotel",
          "radius" : 5000,
          "key" : g_key}


# In[20]:


for index, row in hotel_df.iterrows():
    # get city name, lat, lnt from df
    lat = row["Lat"]
    lng = row["Lng"]
    city_name = row["City"]
    
    # add keyword to params dict
    params["location"] = f"{lat},{lng}"

    # assemble url and make API request
    print(f"Retrieving Results for Index {index}: {city_name}.")
    response = requests.get(base_url, params=params).json()
    
    # extract results
    results = response['results']
    
    # save the hotel to dataframe
    try:
        print(f"Closest hotel in {city_name} is {results[0]['name']}.")
        hotel_df.loc[index, "Hotel Name"] = results[0]['name']

    # if there is no hotel available, show missing field
    except (KeyError, IndexError):
        print("Missing field/result... skipping.")
        
    print("------------")
    
    # Wait 1 sec to make another api request to avoid SSL Error
    time.sleep(1)

# Print end of search once searching is completed
print("-------End of Search-------")


# In[21]:


# Display the hotel dataframe
hotel_df
# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
hotel_info = [info_box_template.format(**row) for index, row in hotel_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[22]:


# Add marker layer and info box content ontop of heat map
markers = gmaps.marker_layer(locations, info_box_content = hotel_info)

# Add the layer to the map
fig.add_layer(markers)

# Display Map
fig


# In[ ]:





# In[ ]:





# In[ ]:




