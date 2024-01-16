#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:00:59 2023

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

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
prj_folder = '/Users/gretam/Documents/'
data_folder = '/Users/gretam/Documents/data/'
c40=data_folder+'c40/t2_population/'
ucdb=data_folder+'ucdb/t2_population/'

#https://population.un.org/wpp/Download/Standard/Population/ 
#20+ percentage of population
pct_adult=54.52968999/100

#%% UCDB FILES
#create an approximate adult pop file for Jakarta using age pyramid info from
#load in population data
jakarta_totalpop_ucdb=rxr.open_rasterio(ucdb+'Jakarta_totalPop.tif',masked=True).squeeze()
print("The crs of your data is:", jakarta_totalpop_ucdb.rio.crs)
print("The nodatavalue of your data is:", jakarta_totalpop_ucdb.rio.nodata)
print("The number of bands for your data is:", jakarta_totalpop_ucdb.rio.count)
print("The shape of your data is:", jakarta_totalpop_ucdb.shape)
print("The spatial resolution for your data is:", jakarta_totalpop_ucdb.rio.resolution())
print(jakarta_totalpop_ucdb.rio.bounds())
print("The metadata for your data is:", jakarta_totalpop_ucdb.attrs)
print(jakarta_totalpop_ucdb)

jakarta_totalpop_ucdb.plot()
plt.show() # show the plot in the ipython console

#get some summary info on data before scaling it to adult pop
tot_pop_mean=np.nanmean(jakarta_totalpop_ucdb.data)
print('mean: ', tot_pop_mean)
tot_pop_min=np.nanmin(jakarta_totalpop_ucdb.data)
print('min: ', tot_pop_min)
tot_pop_max=np.nanmax(jakarta_totalpop_ucdb.data)
print('max: ', tot_pop_max)
tot_pop_std=np.nanstd(jakarta_totalpop_ucdb.data)
print('std: ', tot_pop_std)
tot_pop_total=np.nansum(jakarta_totalpop_ucdb.data)
print('total: ', tot_pop_total)

#scale each pixel to adult pop
jakarta_adult_pop_ucdb=jakarta_totalpop_ucdb*pct_adult

tot_pop_mean=np.nanmean(jakarta_adult_pop_ucdb.data)
print('mean: ', tot_pop_mean)
tot_pop_min=np.nanmin(jakarta_adult_pop_ucdb.data)
print('min: ', tot_pop_min)
tot_pop_max=np.nanmax(jakarta_adult_pop_ucdb.data)
print('max: ', tot_pop_max)
tot_pop_std=np.nanstd(jakarta_adult_pop_ucdb.data)
print('std: ', tot_pop_std)
tot_pop_total_adult=np.nansum(jakarta_adult_pop_ucdb.data)
print('total: ', tot_pop_total)

print(tot_pop_total_adult/tot_pop_total)
jakarta_adult_pop_ucdb.plot()
plt.show() # show the plot in the ipython console

#save as geotiff in correct folder
jakarta_adult_pop_ucdb.rio.to_raster(ucdb+"adult pop/Jakarta.tif")

#%% C40 shapefiles
#create an approximate adult pop file for Jakarta using age pyramid info from
#load in population data
jakarta_totalpop_c40=rxr.open_rasterio(c40+'Jakarta_totalPop.tif',masked=True).squeeze()
print("The crs of your data is:", jakarta_totalpop_c40.rio.crs)
print("The nodatavalue of your data is:", jakarta_totalpop_c40.rio.nodata)
print("The number of bands for your data is:", jakarta_totalpop_c40.rio.count)
print("The shape of your data is:", jakarta_totalpop_c40.shape)
print("The spatial resolution for your data is:", jakarta_totalpop_c40.rio.resolution())
print(jakarta_totalpop_c40.rio.bounds())
print("The metadata for your data is:", jakarta_totalpop_c40.attrs)
print(jakarta_totalpop_c40)

jakarta_totalpop_c40.plot()
plt.show() # show the plot in the ipython console

#get some summary info on data before scaling it to adult pop
tot_pop_mean=np.nanmean(jakarta_totalpop_c40.data)
print('mean: ', tot_pop_mean)
tot_pop_min=np.nanmin(jakarta_totalpop_c40.data)
print('min: ', tot_pop_min)
tot_pop_max=np.nanmax(jakarta_totalpop_c40.data)
print('max: ', tot_pop_max)
tot_pop_std=np.nanstd(jakarta_totalpop_c40.data)
print('std: ', tot_pop_std)
tot_pop_total=np.nansum(jakarta_totalpop_c40.data)
print('total: ', tot_pop_total)

#scale each pixel to adult pop
jakarta_adult_pop_c40=jakarta_totalpop_c40*pct_adult

tot_pop_mean=np.nanmean(jakarta_adult_pop_c40.data)
print('mean: ', tot_pop_mean)
tot_pop_min=np.nanmin(jakarta_adult_pop_c40.data)
print('min: ', tot_pop_min)
tot_pop_max=np.nanmax(jakarta_adult_pop_c40.data)
print('max: ', tot_pop_max)
tot_pop_std=np.nanstd(jakarta_adult_pop_c40.data)
print('std: ', tot_pop_std)
tot_pop_total_adult=np.nansum(jakarta_adult_pop_c40.data)
print('total: ', tot_pop_total)

print(tot_pop_total_adult/tot_pop_total)
jakarta_adult_pop_c40.plot()
plt.show() # show the plot in the ipython console

    
jakarta_adult_pop_c40.rio.to_raster(c40+"adult pop/Jakarta.tif")