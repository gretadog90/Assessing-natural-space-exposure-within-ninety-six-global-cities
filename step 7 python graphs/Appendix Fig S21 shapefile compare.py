#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 16:53:15 2023

@author: gretam
"""
#%% load modules
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#%% file paths

shapes_folder = '/Users/gretam/Documents/data/shapefiles/'
output = '/Users/gretam/Documents/data/ucdb/graphs/'


#%% get data in same geo data frame

# import 2 different city bounds
c40_shapes = gpd.read_file(shapes_folder+'c40_list_selfdefined/c40_list_selfdefined.shp')
ucdb_shapes = gpd.read_file(shapes_folder+'c40_cities/c40_cities.shp')

c40_names=c40_shapes['City'].to_list()
ucdb_names=ucdb_shapes['City'].to_list()
print(set(c40_names) ^ set(ucdb_names))

#for testing individual cities:
c40_names=['Tokyo']

#map
for city in c40_names:
    #pull off just one city at a time
    c40_city_bounds=c40_shapes[c40_shapes['City'] == city]
    ucdb_city_bounds=ucdb_shapes[ucdb_shapes['City'] == city]
    
    print(city)
    #graph both boundaries
    fig, ax = plt.subplots(figsize = (20,16)) 
    c40_city_bounds.geometry.boundary.plot(color='red',edgecolor='k',linewidth = 2,ax=ax)
    ucdb_city_bounds.geometry.boundary.plot(color='blue',edgecolor='k',linewidth = 2,ax=ax)
    plt.suptitle(city+' urban bounds ', fontsize=40)
    plt.title('Blue: ucdb, Red: c40 defined',  fontsize=40)
    plt.show()
    plt.clf()
 

#%% remove Moscow from city list (not a current C40 member city)
c40_names.remove('Moscow')
print(c40_names)

#%% try to combine all these graphs into multipanel image

fig, axs = plt.subplots(nrows=12, ncols=8, figsize=(30, 24))
plt.subplots_adjust(hspace=0.4)
plt.suptitle('Urban Bounds. Blue: UCDB, Red: C40', fontsize=22)
plt.subplots_adjust(top=0.95)

# loop through tickers and axes
for n, city in enumerate(c40_names):
    ax = plt.subplot(12, 8, n + 1)
    # chart formatting
    ax.set_title(city)
    
    c40_city_bounds=c40_shapes[c40_shapes['City'] == city]
    ucdb_city_bounds=ucdb_shapes[ucdb_shapes['City'] == city]
    
    print(city)
    
    c40_city_bounds.geometry.boundary.plot(color='red',edgecolor='k',linewidth = 2,ax=ax)
    ucdb_city_bounds.geometry.boundary.plot(color='blue',edgecolor='k',linewidth = 2,ax=ax)
    
  
filename=output+'ucdbc40shapefile.png'
fig.savefig(filename ,dpi=300, bbox_inches = 'tight')
plt.show()
plt.clf()
    

   

    
