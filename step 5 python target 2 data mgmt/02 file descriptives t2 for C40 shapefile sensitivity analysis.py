#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 12:09:37 2023

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
data_folder = '/Users/gretam/Documents/data/c40/'
output=data_folder+'t2_output/'

mndvi_path=data_folder+'t2_mndvi/'
gba_path=data_folder+'t2_gba/'
pop_path=data_folder+'t2_population/adult pop/'

# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(gba_path)  if not i.startswith('.')]
print(len(c40_list))
print(c40_list)

#%% turn dictionaries into data frames for easier manipulation-- and export as excel sheet
# defining the variables
dict_t2 = {}
for city in c40_list:
    #load in ndvi
    mndvi75=rxr.open_rasterio(mndvi_path+city+'_75.tif',masked=True).squeeze()
    gba=rxr.open_rasterio(gba_path+city+'.tif',masked=True).squeeze()
    pop=rxr.open_rasterio(pop_path+city+'_adultPop.tif',masked=True).squeeze()
    
    #stack so that each row becomes x,y pair with ndvi value
    mndvi75=mndvi75.stack(z=("x", "y"))
    mndvi75_df = pd.DataFrame(mndvi75, columns = ['mndvi75'])
    
    #save the actual coordinates & add to dataframe (only need to do this once)
    index=mndvi75.indexes["z"].to_list()
    mndvi75_df['coords'] = index
    
    #rpeat for green/blue area
    gba=gba.stack(z=("x", "y"))
    gba_df = pd.DataFrame(gba, columns = ['gba'])
    
    #rpeat for pop
    pop=pop.stack(z=("x", "y"))
    pop_df = pd.DataFrame(pop, columns = ['pop'])
    
    #merge all the natural space metrics together 
    merged_df=pd.concat([gba_df, mndvi75_df, pop_df], axis=1)
    dict_t2[city]=merged_df
    
    #save city excel file with just the rows that have data
    merged_subset = merged_df.dropna(subset=['gba', 'mndvi75','pop'], how='all')
    merged_subset.to_csv(output+city+'.csv')