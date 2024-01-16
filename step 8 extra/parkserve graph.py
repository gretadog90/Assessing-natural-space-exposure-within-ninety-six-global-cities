#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 12:04:26 2024

@author: gretam
"""


#%% load modules
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns

#%% plot t2 definitions against parksmart
parksmart = pd.read_csv('/Users/gretam/Documents/Stata/output_ucdb/parkserve_compare.csv',
                        sep='\t')

parksmart_urbanarea=parksmart.loc[parksmart['metric'].isin(['Equitable Spatial Distribution (UCDB)', 'Parkserve (U.S. Census Urban Area)'])]

#%% make graph
sns.set_style("whitegrid")
plt.figure(figsize=(30, 15))
plt.subplots_adjust(hspace=0.5)
fig, ax = plt.subplots()

sns.set(font_scale = .2)
sns.set(style='whitegrid')
a=sns.stripplot(data = parksmart,
              y='city', x='value', ax=ax,
              hue = 'metric').set(xlabel='Measures of natural space access', ylabel='')
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1), title='Measure source')

filename='/Users/gretam/Documents/data/ucdb/graphs/parkserve.svg' 
plt.savefig(filename, format='svg', dpi=300, bbox_inches = "tight")
plt.show()


#%% make graph
sns.set_style("whitegrid")
plt.figure(figsize=(30, 15))
plt.subplots_adjust(hspace=0.5)
fig, ax = plt.subplots()

sns.set(font_scale = .2)
sns.set(style='whitegrid')
a=sns.stripplot(data = parksmart_urbanarea,
              y='city', x='value', ax=ax,
              hue = 'metric', palette=['lightcoral','teal']).set(xlabel='Measures of natural space access', ylabel='')
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1), title='Measure source')

filename='/Users/gretam/Documents/data/ucdb/graphs/parkserve_ua.svg' 
plt.savefig(filename, format='svg', dpi=300, bbox_inches = "tight")
plt.show()




