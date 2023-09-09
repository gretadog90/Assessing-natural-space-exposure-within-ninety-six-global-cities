#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:50:35 2023

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
data_folder = '/Users/gretam/Documents/data/ucdb/'
output=data_folder+'t2_output/'


ndvi_path=data_folder+'t2_ndvi/'
ga_path=data_folder+'t2_ga/'
mndvi_path=data_folder+'t2_mndvi/'
gba_path=data_folder+'t2_gba/'
pop_path=data_folder+'t2_population/adult pop/'

# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(ndvi_path)  if not i.startswith('.')]
print(len(c40_list))
print(c40_list)

#%% load data and just do some basic checks that info is as we expect and that 
# all the data sets for each city share the same shape, resolution, bounds, etc.ß

# loop through geotiffs to print out some info
for file in c40_list:
    ndvi=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    ga=rxr.open_rasterio(ga_path+file+'.tif',masked=True).squeeze()
    mndvi=rxr.open_rasterio(mndvi_path+file+'.tif',masked=True).squeeze()
    gba=rxr.open_rasterio(gba_path+file+'.tif',masked=True).squeeze()
    pop=rxr.open_rasterio(pop_path+file+'.tif',masked=True).squeeze()
    print(file)
    print("The crs of your data is:", ndvi.rio.crs)
    print("The nodatavalue of your data is:", ndvi.rio.nodata)
    print("The number of bands for your data is:", ndvi.rio.count)
    print("The shape of your data is:", ndvi.shape)
    print("The spatial resolution for your data is:", ndvi.rio.resolution())
    print(ndvi.rio.bounds())
    #should all be same for ga
    print(ndvi.rio.crs==ga.rio.crs)
    print(ndvi.rio.shape==ga.rio.shape)
    print(ndvi.rio.resolution()==ga.rio.resolution())
    print(ndvi.rio.bounds()==ga.rio.bounds())
    #should all be same for mndvi
    print(ndvi.rio.crs==mndvi.rio.crs)
    print(ndvi.rio.shape==mndvi.rio.shape)
    print(ndvi.rio.resolution()==mndvi.rio.resolution())
    print(ndvi.rio.bounds()==mndvi.rio.bounds())
    #should all be same for gba
    print(ndvi.rio.crs==gba.rio.crs)
    print(ndvi.rio.shape==gba.rio.shape)
    print(ndvi.rio.resolution()==gba.rio.resolution())
    print(ndvi.rio.bounds()==gba.rio.bounds())
    #should all be same for pop
    print(ndvi.rio.crs==pop.rio.crs)
    print(ndvi.rio.shape==pop.rio.shape)
    print(ndvi.rio.resolution()==pop.rio.resolution())
    print(ndvi.rio.bounds()==pop.rio.bounds())
    #get name of of variable where data stored
    print("The metadata for your data is:", ndvi.attrs)
    print("The metadata for your data is:", ga.attrs)
    print("The metadata for your data is:", mndvi.attrs)
    print("The metadata for your data is:", gba.attrs)
    print("The metadata for your data is:", pop.attrs)


#%% turn dictionaries into data frames for easier manipulation-- and export as excel sheet
# defining the variables
dict_t2 = {}
for city in c40_list:
    #load in ndvi
    ndvi=rxr.open_rasterio(ndvi_path+city+'.tif',masked=True).squeeze()
    ga=rxr.open_rasterio(ga_path+city+'.tif',masked=True).squeeze()
    mndvi=rxr.open_rasterio(mndvi_path+city+'.tif',masked=True).squeeze()
    mndvi75=rxr.open_rasterio(mndvi_path+city+'_75.tif',masked=True).squeeze()
    mndvi90=rxr.open_rasterio(mndvi_path+city+'_90.tif',masked=True).squeeze()
    gba=rxr.open_rasterio(gba_path+city+'.tif',masked=True).squeeze()
    pop=rxr.open_rasterio(pop_path+city+'.tif',masked=True).squeeze()


    # create a 4 panel image of these natural space vars
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout=True, sharey=True, sharex=True)

    ga.plot(ax=ax1, cmap="Greens", vmin=0, vmax=1)
    ndvi.plot(ax=ax2,cmap="Greens", vmin=0, vmax=1)
    gba.plot(ax=ax3, cmap="Greens", vmin=0, vmax=1)
    mndvi.plot(ax=ax4,cmap="Greens", vmin=0, vmax=1)

    #title each subplot 
    ax1.set_title('A. Landcover: green area', fontsize=8)
    ax2.set_title('B. NDVI', fontsize=8)
    ax3.set_title('C. Landcover: green and blue area', fontsize=8) 
    ax4.set_title('D. NDVI plus water', fontsize=8) 
      
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

    filename=output+city+'.png' 
    fig.savefig(filename ,dpi=300,bbox_inches = 'tight')
    plt.clf()
    
    #stack so that each row becomes x,y pair with ndvi value
    ndvi=ndvi.stack(z=("x", "y"))
    #save to data frame
    ndvi_df = pd.DataFrame(ndvi, columns = ['ndvi'])
    #save the actual coordinates & add to dataframe (only need to do this once)
    index=ndvi.indexes["z"].to_list()
    ndvi_df['coords'] = index
    
    #repeat for green area
    ga=ga.stack(z=("x", "y"))
    ga_df = pd.DataFrame(ga, columns = ['ga'])
    
    #repeat for our modified ndvi metric
    mndvi=mndvi.stack(z=("x", "y"))
    mndvi_df = pd.DataFrame(mndvi, columns = ['mndvi'])
    
    #repeat for our modified ndvi metric
    mndvi75=mndvi75.stack(z=("x", "y"))
    mndvi75_df = pd.DataFrame(mndvi75, columns = ['mndvi75'])
    
    #repeat for our modified ndvi metric
    mndvi90=mndvi90.stack(z=("x", "y"))
    mndvi90_df = pd.DataFrame(mndvi90, columns = ['mndvi90'])
    
    #rpeat for green/blue area
    gba=gba.stack(z=("x", "y"))
    gba_df = pd.DataFrame(gba, columns = ['gba'])
    
    #rpeat for pop
    pop=rxr.open_rasterio(pop_path+city+'.tif',masked=True).squeeze()
    pop=pop.stack(z=("x", "y"))
    pop_df = pd.DataFrame(pop, columns = ['pop'])
    
    #merge all the natural space metrics together 
    merged_df=pd.concat([ndvi_df, ga_df, gba_df, mndvi_df, mndvi75_df, mndvi90_df, pop_df], axis=1)
    dict_t2[city]=merged_df
    
    #save city excel file with just the rows that have data
    merged_subset = merged_df.dropna(subset=['ndvi', 'ga', 'gba', 'mndvi','mndvi75', 'mndvi90', 'pop'], how='all')
    merged_subset.to_csv(output+city+'.csv')