#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:47:23 2023

@author: gretam
"""
#%% load modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
import os
import seaborn as sns

#%% file paths
data_folder = '/Users/gretam/Documents/data/ucdb/'
import_folder = '/Users/gretam/Documents/data/ucdb/t1_output/'
output=data_folder+'graphs/'


# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(data_folder+'t1_ndvi/')  if not i.startswith('.')]
print(len(c40_list))
print(c40_list)


c40=pd.read_csv('/Users/gretam/Documents/Stata/output_ucdb/appendixA.csv') 
t1=pd.read_csv('/Users/gretam/Documents/Stata/output_ucdb/ols_summary_t1.csv') 

# Get a list of lists by grouping on 'region' column and get List for 'city' column
#now there is a list of all the cities in each region
cities = c40.groupby('region')['city'].apply(list).to_dict()
print(cities)   

for key, value in cities.items(): 
    print(key)
    print(value)
    print(len(value))

#%% create density scatters with OLS line (Africa)
cities_af=['Abidjan', 'Accra', 'Addis Ababa', 'Cape Town', 'Dakar', 'Dar es Salaam', 
                 'Durban eThekwini', 'Ekurhuleni', 'Freetown', 'Johannesburg', 'Lagos', 'Nairobi', 'Tshwane']

plt.figure(figsize=(25, 30))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.05, right=.95)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: Africa", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cities_af):
    # add a new subplot iteratively
    ax = plt.subplot(5, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    if city=="Durban eThekwini":
        ax.set_ylabel('NDVI', fontsize=28, labelpad=20)
    else:
        ax.set_ylabel('')
    if city=="Lagos":
        ax.set_xlabel('Proportion green area', fontsize=28, labelpad=400)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.85, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=28, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'Africa_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  

#%% create density scatters with OLS line (Central East Asia)
cities_cea=['Beijing', 'Chengdu', 'Dalian', 'Fuzhou', 'Guangzhou', 'Hangzhou', 
           'Hong Kong', 'Nanjing', 'Qingdao', 'Shanghai', 'Shenzhen', 'Wuhan', 'Zhenjiang']

plt.figure(figsize=(25, 30))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.05, right=.95)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: Central East Asia", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cities_cea):
    # add a new subplot iteratively
    ax = plt.subplot(5, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    if city=="Hong Kong":
        ax.set_ylabel('NDVI', fontsize=25, labelpad=20)
    else:
        ax.set_ylabel('')
    if city=="Shenzhen":
        ax.set_xlabel('Proportion green area', fontsize=25, labelpad=400)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.85, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=25, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'CentralEastAsia_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  

#%% create density scatters with OLS line (East, Southeast Asia & Oceana)
cites_esao=['Auckland', 'Bangkok', 'Hanoi', 'Ho Chi Minh City', 'Jakarta', 'Kuala Lumpur', 
            'Melbourne', 'Quezon City', 'Seoul', 'Singapore', 'Sydney', 'Tokyo', 'Yokohama']

plt.figure(figsize=(25, 30))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.05, right=.95)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: East, Southeast Asia & Oceania", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cites_esao):
    # add a new subplot iteratively
    ax = plt.subplot(5, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    if city=="Melbourne":
        ax.set_ylabel('NDVI', fontsize=25, labelpad=20)
    else:
        ax.set_ylabel('')
    if city=="Sydney":
        ax.set_xlabel('Proportion green area', fontsize=25, labelpad=400)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.85, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=25, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'ESEAsiaOceania_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  


#%% create density scatters with OLS line (Europe)
cities_eur=['Amsterdam', 'Athens', 'Barcelona', 'Berlin', 'Copenhagen', 'Heidelberg', 
            'Istanbul', 'Lisbon', 'London', 'Madrid', 'Milan', 'Oslo', 'Paris', 'Rome', 
            'Rotterdam', 'Stockholm', 'Tel Aviv Yafo', 'Venice', 'Warsaw']

plt.figure(figsize=(28, 30))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.05, right=.95)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: Europe", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cities_eur):
    # add a new subplot iteratively
    ax = plt.subplot(5, 4, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    if city=="London":
        ax.set_ylabel('NDVI', fontsize=28, labelpad=20)
    else:
        ax.set_ylabel('')
    if city=="Venice":
        ax.set_xlabel('Proportion green area', fontsize=28, labelpad=20, loc="right")
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.85, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=28, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'Europe_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  

#%% create density scatters with OLS line (Latin America)
cites_latam=['Bogota', 'Buenos Aires', 'Curitiba', 'Guadalajara', 'Lima', 'Medellin', 
            'Mexico City', 'Quito', 'Rio de Janeiro', 'Salvador', 'Santiago', 'Sao Paulo']


plt.figure(figsize=(25, 30))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.10, right=.90)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: Latin America", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cites_latam):
    # add a new subplot iteratively
    ax = plt.subplot(4, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    if city=="Guadalajara":
        ax.set_ylabel('NDVI', fontsize=25, labelpad=20, loc='bottom')
    else:
        ax.set_ylabel('')
    if city=="Santiago":
        ax.set_xlabel('Proportion green area', fontsize=25, labelpad=20)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.92, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=25, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'LatAm_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  

#%% create density scatters with OLS line (North America)
cities_na=['Austin', 'Boston', 'Chicago', 'Houston', 'Los Angeles', 'Miami', 'Montreal', 
           'New Orleans', 'New York City', 'Philadelphia', 'Phoenix', 'Portland', 
           'San Francisco', 'Seattle', 'Toronto', 'Vancouver', 'Washington DC']

plt.figure(figsize=(25, 32))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.05, right=.95)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: North America", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cities_na):
    # add a new subplot iteratively
    ax = plt.subplot(6, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    if city=="Montreal":
        ax.set_ylabel('NDVI', fontsize=25, labelpad=20, loc='bottom')
    else:
        ax.set_ylabel('')
    if city=="Washington DC":
        ax.set_xlabel('Proportion green area', fontsize=25, labelpad=20)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.85, 0.05, 0.03, 0.12])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=25, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'NAmerica_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  


#%% create density scatters with OLS line (South and West Asia)
cities_swa=['Amman', 'Bengaluru', 'Chennai', 'Delhi NCT', 'Dhaka North and South', 
            'Dubai', 'Karachi', 'Kolkata', 'Mumbai']

plt.figure(figsize=(25, 25))
plt.subplots_adjust(hspace=0.2, top=.93, bottom=.05, left=.10, right=.90)

sns.set(style='white')

plt.suptitle("Quality Total Cover Regression Models: South and West Asia", fontsize=40, y=0.98)

# loop through the length of tickers and keep track of index
for n, city in enumerate(cities_swa):
    # add a new subplot iteratively
    ax = plt.subplot(3, 3, n + 1)
    fig=ax.get_figure()
        
    #subset to non-null values of ga and ndvi (some are NaN because are water)
    target1=pd.read_csv(import_folder+city+'.csv') 
    target1=target1.dropna(subset=['ndvi', 'ga'], how='any')
    
    #get fit line
    a=t1[t1['city']==city]['b_cons'].values
    b=t1[t1['city']==city]['b_ga'].values
    x=target1['ga']
    y=target1['ndvi']
    ols=a+(b*x)
     
    xy = np.vstack([target1["ga"], target1["ndvi"]])
    kernel = stats.gaussian_kde(xy)(xy)
   
    plot=sns.scatterplot(data=target1, x="ga", y="ndvi", c=kernel,
        cmap="viridis", ax=ax)
    ax.plot(x, ols, '-r', lw=3)
    ax.set(xlim=(0, 1))
    ax.set(ylim=(0, 1))
    ax.set_title(city, fontsize=25, weight='bold')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    if city=="Delhi NCT":
        ax.set_ylabel('NDVI', fontsize=25, labelpad=20)
    else:
        ax.set_ylabel('')
    if city=="Kolkata":
        ax.set_xlabel('Proportion green area', fontsize=25, labelpad=20)
    else:
        ax.set_xlabel('')

#creates a color bar rectangle
cax = fig.add_axes([0.92, 0.05, 0.03, 0.15])
sm = plt.cm.ScalarMappable(cmap='viridis')
cbar=fig.colorbar(sm, cax=cax)
cbar.ax.set_ylabel('Kernel density', size=25, labelpad=20)
cbar.ax.tick_params(labelsize=15)


filename=output+'SWAsia_ols_t1.png' 
plt.savefig(filename)
plt.show()
plt.clf()  