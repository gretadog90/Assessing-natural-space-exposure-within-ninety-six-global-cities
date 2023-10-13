#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:56:43 2023

@author: gretam
"""

#%% load modules
import rasterio as rio
from rasterio.plot import show
import xarray as xr
import rioxarray as rxr
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
#from matplotlib_scalebar.scalebar import ScaleBar
#from sklearn.metrics.pairwise import haversine_distances
import cartopy.crs as ccrs

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
prj_folder = '/Users/gretam/Documents/data/ucdb/'

ndvi=rxr.open_rasterio(prj_folder+'t1_ndvi/Washington DC.tif',masked=True).squeeze()
ga=rxr.open_rasterio(prj_folder+'t1_ga/Washington DC.tif',masked=True).squeeze()
mndvi=rxr.open_rasterio(prj_folder+'t2_mndvi/Washington DC_75.tif',masked=True).squeeze()
gba=rxr.open_rasterio(prj_folder+'t2_gba/Washington DC.tif',masked=True).squeeze()

#%%some data mgmt for graph labels and colors
ndvi.attrs["long_name"] = "NDVI (100m mean)"
ga.attrs["long_name"] = "Proportion green area     (100m mean)"
mndvi.attrs["long_name"] = "Proportion w/ access in 1000m buffer (100m mean)"
gba.attrs["long_name"] = "Proportion w/ access in 1000m buffer (100m mean)"


heading=['Target 1: Quality Total Cover', 'Target 2: Equitable Spatial Distribution']

SMALL_SIZE = 7
MEDIUM_SIZE = 8
BIGGER_SIZE = 10

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title


#%%create multipanel image for methods section
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=True, sharey=True, sharex=True)

ga.plot(ax=ax1, cmap="Greens", vmin=0, vmax=1)
ndvi.plot(ax=ax2,cmap="Greens", vmin=0, vmax=1)
gba.plot(ax=ax3, cmap="Greens", vmin=0, vmax=1)
mndvi.plot(ax=ax4,cmap="Greens", vmin=0, vmax=1)

#title each subplot 
ax1.set_title('a. Landcover: green area                           ', fontsize=8, weight='bold')
ax2.set_title('b. NDVI: green space                                        ', fontsize=8, weight='bold')
ax3.set_title('c. Landcover: green and blue area            ', fontsize=8, weight='bold')
ax4.set_title('d. NDVI: natural space                                     ', fontsize=8, weight='bold') 
  
#remove all the individual plot labels
ax1.set_xlabel('')
ax1.set_ylabel('')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax3.set_xlabel('')
ax3.set_ylabel('')
ax4.set_ylabel('')
ax4.set_xlabel('')

#create common x/y labels
fig.supxlabel('latitude', fontsize=8)
fig.supylabel('longitude', fontsize=8)


plt.show() 

filename=prj_folder+'graphs/methods figure.png' 
fig.savefig(filename ,dpi=300,bbox_inches = 'tight')
plt.clf()

