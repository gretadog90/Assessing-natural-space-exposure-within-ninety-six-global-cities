#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 12:15:54 2023

@author: gretam
"""

#%% load modules
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/'
results = '/Users/gretam/Documents/Stata/output_ucdb/'
output='/Users/gretam/Documents/data/ucdb/graphs/'


SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 14

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title

#%% get data in same geo data frame
# import shapefile using geopandas
c40_smod_shapes = gpd.read_file(data_folder+'shapefiles/c40_cities/c40_cities.shp')
#replace spelling error
c40_smod_shapes['Region']=c40_smod_shapes['Region'].str.replace('Oceana', 'Oceania')

#load in city means from full run to get the NDVI means
target1=pd.read_csv(results+'ols_summary_t1.csv') 

#create new City var to match naming in shapefile dataset
target1['City'] = target1['city']

#merge the city centroid and name file with the city means
c40_t1=pd.merge(left=target1, right=c40_smod_shapes, how='left', on='City')

#load in city means from full run to get the NDVI means
target2=pd.read_csv(results+'ols_summary_t2.csv') 

#create new City var to match naming in shapefile dataset
target2['City'] = target2['city']

#merge the city centroid and name file with the city means
c40_t2=pd.merge(left=target2, right=c40_smod_shapes, how='left', on='City')


#%% make graph
plt.figure(figsize=(30, 15))
plt.subplots_adjust(hspace=0.5)
fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle("Quality Total Cover Regression Fit Statistics by Region", fontsize=13, y=0.98)

regions=["Africa", "Central East Asia", "East, Southeast Asia & Oceania", "Europe", "Latin America", "North America", "South and West Asia"]
colors=['plum', 'mediumaquamarine', 'salmon', 'steelblue', 'olivedrab', 'burlywood', 'palevioletred']
color_dict=dict(zip(regions, colors))

#order is regional mean low to high
order=['Latin America', 'Central East Asia', 'Africa', 'South and West Asia', 'East, Southeast Asia & Oceania', 'Europe', 'North America']

#sns.set(font_scale = .7)
sns.set(style='whitegrid')
a=sns.stripplot(data = c40_t1,
              y='Region', x='adjr2',order=order, ax=ax1,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='R2', ylabel='',
              title='A. Coefficient of determination')
ax1.set(xlim=(0, 1))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           
ax1.legend().remove()


#regional mean low to high
b=sns.stripplot(data = c40_t1,
              y='Region', x='rmse',ax=ax2,order=order,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='rmse',
                     title='B. Root mean square error     ', ylabel='', 
                     yticks=[])                                
ax2.set(xlim=(0, 1))
ax2.legend().remove()
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           

filename=output+'fit stats T1.png' 
plt.savefig(filename ,dpi=300, bbox_inches = "tight")
plt.show()

#%% make graph
plt.figure(figsize=(30, 15))
plt.subplots_adjust(hspace=0.5)
fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle("Equitable Spatial Distribution Regression Fit Statistics by Region", fontsize=13, y=0.98)

#sns.set(font_scale = .7)
sns.set(style='whitegrid')
a=sns.stripplot(data = c40_t2,
              y='Region', x='adjr2_75',order=order, ax=ax1,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='R2', ylabel='',
              title='A. Coefficient of determination')
ax1.set(xlim=(0, 1))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           
ax1.legend().remove()


#regional mean low to high
b=sns.stripplot(data = c40_t2,
              y='Region', x='rmse_75',ax=ax2,order=order,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='rmse',
                     title='B. Root mean square error     ', ylabel='', 
                     yticks=[])                                
ax2.set(xlim=(0, 1))
ax2.legend().remove()
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           

filename=output+'fit stats T2.png' 
plt.savefig(filename ,dpi=300, bbox_inches = "tight")
plt.show()