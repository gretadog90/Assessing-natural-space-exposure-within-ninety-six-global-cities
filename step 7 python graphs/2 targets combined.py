#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 10:32:10 2023

@author: gretam
"""

#%% load modules
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/'
prj_folder = '/Users/gretam/Documents/'

#%% get data in same geo data frame
# import shapefile using geopandas
c40_smod_shapes = gpd.read_file(data_folder+'shapefiles/c40_cities/c40_cities.shp')
#replace spelling error
c40_smod_shapes['Region']=c40_smod_shapes['Region'].str.replace('Oceana', 'Oceania')

#load in city means from full run to get the NDVI means
target1=pd.read_csv('/Users/gretam/Documents/Stata/output ucdb/city_summary_t1.csv') 

#create new City var to match naming in shapefile dataset
target1['City'] = target1['city']

#merge the city centroid and name file with the city means
c40_t1=pd.merge(left=target1, right=c40_smod_shapes, how='left', on='City')

#load in city means from full run to get the NDVI means
target2=pd.read_csv('/Users/gretam/Documents/Stata/output ucdb/city_summary_t2.csv') 

#create new City var to match naming in shapefile dataset
target2['City'] = target2['city']

#merge the city centroid and name file with the city means
c40_t2=pd.merge(left=target2, right=c40_smod_shapes, how='left', on='City')


#%% make graph
plt.figure(figsize=(30, 15))
plt.subplots_adjust(hspace=0.5)
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("C40 Urban Nature Declaration Target Status", fontsize=14, y=0.98)

regions=["Africa", "Central East Asia", "East, Southeast Asia & Oceania", "Europe", "Latin America", "North America", "South and West Asia"]
colors=['plum', 'mediumaquamarine', 'salmon', 'steelblue', 'olivedrab', 'burlywood', 'palevioletred']
color_dict=dict(zip(regions, colors))

#order is regional mean low to high
order=['Latin America', 'Central East Asia', 'Africa', 'South and West Asia', 'East, Southeast Asia & Oceania', 'Europe', 'North America']

sns.set(font_scale = .7)
sns.set(style='whitegrid')
a=sns.stripplot(data = c40_t1,
              y='Region', x='ga_mean', order=order, ax=ax1,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='Proportion Green Area', ylabel='',
              title='A. Quality Total Cover            ')
            
ax1.legend().remove()
ax1.axvline(0.3, ls='--', c='yellowgreen')
ax1.axvline(0.4, ls='--', c='darkolivegreen')


#regional mean low to high
b=sns.stripplot(data = c40_t2,
              y='Region', x='t2', order=order,ax=ax2,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='Proportion of Population',
                     title='B. Equitable Spatial Distribution', ylabel='', 
                     yticks=[])                                
ax2.axvline(0.7, ls='--', c='midnightblue')

ax2.legend().remove()

filename=data_folder+'output/Targets combined.png' 
plt.savefig(filename ,dpi=300, bbox_inches = "tight")
plt.show()