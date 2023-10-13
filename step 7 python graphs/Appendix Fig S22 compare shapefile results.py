#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 13:37:02 2023

@author: gretam


APPENDIX E
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
from textwrap import wrap

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/'
results = '/Users/gretam/Documents/Stata/output_ucdb/'
output='/Users/gretam/Documents/data/ucdb/graphs/'


plt.rc('font', size=4)          # controls default text sizes
plt.rc('axes', titlesize=4)     # fontsize of the axes title
plt.rc('axes', labelsize=4)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=4)    # fontsize of the tick labels
plt.rc('ytick', labelsize=4)    # fontsize of the tick labels
plt.rc('legend', fontsize=4)    # legend fontsize
plt.rc('figure', titlesize=6)  # fontsize of the figure title


#load in city means from full run to get the NDVI means
appendixc=pd.read_csv('/Users/gretam/Documents/Stata/output_ucdb/appendixE.csv') 
#%% graph

sns.set(style='whitegrid')

plt.figure(figsize=(20, 15))
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.tight_layout(pad=2.0)
fig.subplots_adjust(top=0.8)


#fig.suptitle("Target-equivalent natural space by urban boundary definition", fontsize=12, y=0.98)

#wrap panel titles
titles=['a. Estimated target equivalent NDVI at 30% green area' ,'b. Estimated target equivalent natural space NDVI at 70% population access' ]
wrapped_titles = [ '\n'.join(wrap(t, 35)) for t in titles ]


#Panel A

a=sns.scatterplot(data = appendixc,
              y='t1_p_ndvi_30_ucdb', x='t1_p_ndvi_30_c40', ax=ax1,
              hue='ucdb_bigger_t1', palette=['mediumaquamarine','thistle']).set(xlabel='C40 shapefiles', 
              ylabel='UCDB shapefiles', title=wrapped_titles[0])
ax1.get_legend().remove()
ax1.set(xlim=(0, 1), ylim=(0, 1))
ax1.axline([.2, .2], [.55, .55])
 
#Panel B
b=sns.scatterplot(data = appendixc,
              y='t2_p_mndvi_70_ucdb', x='t2_p_mndvi_70_c40', ax=ax2,
              hue='ucdb_bigger_t2', palette=['mediumaquamarine','thistle']).set(xlabel='C40 shapefiles', 
              ylabel='UCDB shapefiles', title=wrapped_titles[1])
ax2.set(xlim=(0, 1), ylim=(0, 1))
ax2.get_legend().remove()


#custom legend
box = ax2.get_position()
legend_elements = [Line2D([0], [0], marker='o', color='mediumaquamarine', label='C40',
                          markerfacecolor='mediumaquamarine', markersize=8),
                   Line2D([0], [0], marker='o', color='thistle', label='UCDB',
                          markerfacecolor='thistle', markersize=8)]

ax2.legend(handles=legend_elements, loc='lower right', title='Bigger shapefile',
          bbox_to_anchor=(1, 0), fontsize=6)
ax2.axline([.2, .2], [.55, .55])

filename=output+'compare ucdb and c40.png' 
plt.savefig(filename ,dpi=300)
plt.show()


