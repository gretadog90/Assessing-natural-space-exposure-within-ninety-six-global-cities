#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 12:28:20 2023

@author: gretam

PAPER 1 FIGURE
Distribution of NDVI Across C40 Cities by Region

"""

#%% load modules
import rasterio as rio
from rasterio.plot import show
import rioxarray as rxr
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
from rasterio.merge import merge
from numpy import nan
import seaborn as sns


#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
prj_folder = '/Users/gretam/Documents/'
data_folder = '/Users/gretam/Documents/data/ucdb/'
ndvi_path=data_folder+'t1_ndvi/'
output=data_folder+'graphs/'


SMALL_SIZE = 12
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title

# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(ndvi_path)  if not i.startswith('.')]
print(len(c40_list))

c40_list.remove('Moscow') #no longer c40

#%%flatten all the ndvi pixel values and assign to regions for regional plot
greenspace = dict()

#loop through the c40 cities
for file in c40_list:
    ndvi=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    ndvi=ndvi.to_numpy()
    ndvi.flatten()
    ndvi= ndvi[~np.isnan(ndvi)]
    greenspace[file] =ndvi    

greenspace = pd.DataFrame(greenspace.items(), columns = ['City', 'ndvi'])

greenspace = greenspace.explode('ndvi')
greenspace['ndvi'] = greenspace['ndvi'].astype('float')

# merge the c40 city list with these summary stats for graphing
# import shapefile using geopandas
c40_smod_shapes = gpd.read_file(prj_folder+'data/shapefiles/c40_cities/c40_cities.shp')
#replace spelling error
c40_smod_shapes['Region']=c40_smod_shapes['Region'].str.replace('Oceana', 'Oceania')
c40_smod_shapes['color']=""

#merge with city regional info
c40=pd.merge(left=greenspace, right=c40_smod_shapes, how='left', on='City')


#%%arrange data by redion and median ndvi

m = c40.groupby(['Region', 'City'])['ndvi'].apply(np.median)
m.name = 'median'
c40=c40.join(m, on=['Region', 'City'])
c40=c40.sort_values(by=['Region', 'median'])

#%%create multipanel image with ALL regions in one plot
#get rid of grey background
sns.set(style='white')

#control which colors each panel shows up as
regions=["Africa", "Central East Asia", "East, Southeast Asia & Oceania", "Europe", "Latin America", "North America", "South and West Asia"]
colors=['plum', 'mediumaquamarine', 'salmon', 'steelblue', 'olivedrab', 'burlywood', 'palevioletred']
color_dict=dict(zip(regions, colors))
print(color_dict)

#set up panel titles
letters=['a. ', 'b. ', 'c. ', 'd. ', 'e. ', 'f. ', 'g. ']
letter_dict=dict(zip(regions, letters))
print(letter_dict)

plt.figure(figsize=(15, 20))
plt.subplots_adjust(hspace=0.25)

sns.set(style='white')

# loop through the length of tickers and keep track of index
for n, region in enumerate(regions):
    # add a new subplot iteratively
    ax = plt.subplot(4, 2, n + 1)
    fig=ax.get_figure()
    b = sns.violinplot(x='ndvi', y='City', data=c40[c40["Region"]==region], cut=0,
                   inner="quartile",xlabel=None,ylabel=None, color=color_dict[region])
    b.axes.set_title(letter_dict[region]+region,fontsize=17, weight='bold', loc='left')
    b.set_xlabel("NDVI",fontsize=12)
    b.set_ylabel("",fontsize=0)
    b.tick_params(labelsize=13)
    plt.grid() 

fig.tight_layout()
fig.subplots_adjust(top=0.95)

 
filename=output+'ndvi_violin_region.svg' 
plt.savefig(filename, format='svg', dpi=300)
plt.show()
plt.clf() 
