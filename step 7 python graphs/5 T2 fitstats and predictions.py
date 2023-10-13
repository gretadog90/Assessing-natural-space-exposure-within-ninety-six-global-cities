#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:58:07 2023

@author: gretam
"""
#%% load modules
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/'
results = '/Users/gretam/Documents/Stata/output_ucdb/'
output='/Users/gretam/Documents/data/ucdb/graphs/'

#%% get data in same geo data frame
# import shapefile using geopandas
c40_smod_shapes = gpd.read_file(data_folder+'shapefiles/c40_cities/c40_cities.shp')

#replace spelling error
c40_smod_shapes['Region']=c40_smod_shapes['Region'].str.replace('Oceana', 'Oceania')

#create a centroid column for plotting the cities as a dot
c40_smod_shapes["centroid"]=c40_smod_shapes.geometry.centroid.to_crs(epsg=4326)

#load in city means from full run to get the NDVI means
target2=pd.read_csv(results+'ols_summary_t2.csv') 

#create new City var to match naming in shapefile dataset
target2['City'] = target2['city']

#change size of dots based on model fit 
target2['size'] = 20
target2.loc[(target2['adjr2_75'] > .5), 'size'] = 65
print(target2)

#merge the city centroid and name file with the city means
c40_t2=pd.merge(left=target2, right=c40_smod_shapes, how='left', on='City')

#turn data frame into a geo data frame so that it recognizes the geometry
gdf = gpd.GeoDataFrame(c40_t2, geometry="centroid")

#%% make graph
fig=plt.figure(figsize=(18, 12))
plt.subplots_adjust(hspace=0.25)

fig.suptitle("Target 2: Equitable Spatial Distribution", fontsize=20, y=0.95)

# Plot 1
ax1 =  plt.subplot2grid((2, 2), (0, 0), colspan=1)
regions=["Africa", "Central East Asia", "East, Southeast Asia & Oceania", "Europe", "Latin America", "North America", "South and West Asia"]
colors=['plum', 'mediumaquamarine', 'salmon', 'steelblue', 'olivedrab', 'burlywood', 'palevioletred']
color_dict=dict(zip(regions, colors))

#order is regional mean low to high
order=['Latin America', 'Central East Asia', 'Africa', 'South and West Asia', 'East, Southeast Asia & Oceania', 'Europe', 'North America']

sns.set(style='whitegrid')
a=sns.stripplot(data = c40_t2,
              y='Region', x='adjr2_75',order=order, ax=ax1,s=8,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='R2', ylabel='')
ax1.set(xlim=(.2, 1))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           
ax1.legend().remove()

#all the defaults set above get messed up in multipanel so setting sizes explicitly here
ax1.set_title('a. Coefficient of determination', loc='left', fontdict={'fontsize': 16}, weight='bold')

for tick in ax1.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)

l1 = ax1.get_xlabel()

ax1.set_xlabel(l1, fontsize=15)
       
ax2=plt.subplot2grid((2, 2), (0, 1), colspan=1)

#regional mean low to high
b=sns.stripplot(data = c40_t2,
              y='Region', x='rmse_75',ax=ax2,order=order, s=8,
              hue = 'Region', jitter=False, 
              palette=color_dict).set(xlabel='rmse', ylabel='', 
                     yticks=[])                                
ax2.set(xlim=(0, .4))
ax2.legend().remove()
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))           
ax2.set_title('b. Root mean square error', loc='left', fontdict={'fontsize': 16}, weight='bold')
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)

l = ax2.get_xlabel()
ax2.set_xlabel(l, fontsize=15)
    
# Plot 3
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)


#load in world shape file for background
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world=world[world['continent']!='Antarctica']

world.plot(ax=ax3, edgecolor='black',color='white')
ax3.tick_params(labelsize=0)
ax3.grid(False)

ax3=gdf.plot(column='mndvip_70_75', cmap='cool', ax=ax3, marker='o',markersize=gdf['size'])
ax3.set_title('c. Estimated natural spaceNDVI values equivalent to meeting Target 2', loc='left', fontdict={'fontsize': 16}, weight='bold')
ax3.axis('off')

#make colorbar and label for top (adj R2 graphs)
cmap ='cool'
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

cax = fig.add_axes([0.25, 0.1, 0.5, 0.01])

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []
cbar=fig.colorbar(sm, cax=cax, spacing="proportional", orientation='horizontal')
cbar.set_label('Natural space NDVI', labelpad=.0001, fontsize=15)
cbar.ax.tick_params(labelsize=14)

filename=output+'target2 model results.png' 
plt.savefig(filename ,dpi=300, bbox_inches = "tight")
plt.show()

