# -*- coding: utf-8 -*-
"""001_Time Series Data Analysis and Exploratory Analysis .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mg_-93pqvR680fQZDeeDqjF2KTEWIJC4

# **001 Importing Dependencies**
"""

!pip install download

from __future__ import absolute_import,division,print_function,unicode_literals

import seaborn as sns

import matplotlib as mlp
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import os 
from datetime import datetime

from download import download

mlp.rcParams['figure.figsize'] = (8,6)
mlp.rcParams['axes.grid'] = False

"""# **002_Download and Load the datasets**

### beijing city county data import Dingling
"""

path = download('https://archive.ics.uci.edu/ml/machine-learning-databases/00501/PRSA2017_Data_20130301-20170228.zip', 'tmp/aq', kind='zip')

df = pd.read_csv('/content/tmp/aq/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv', encoding = 'ISO-8859-1')

df.head()

df.shape

df.columns

"""## **Target variable in this project is PM2.5**

### What is Particulate Matter 2.5 (PM2.5)?

The term fine particles, or particulate matter 2.5 (PM2.5), refers to tiny particles or droplets in the air that are two and one half microns or less in width. Like inches, meters and miles, a micron is a unit of measurement for distance. There are about 25,000 microns in an inch. The widths of the larger particles in the PM2.5 size range would be about thirty times smaller than that of a human hair. The smaller particles are so small that several thousand of them could fit on the period at the end of this sentence
"""

df.info()

def convert_to_date(x):
  return datetime.strptime(x, '%Y %m %d %H')

"""Refer link for strptime: https://www.geeksforgeeks.org/python-datetime-strptime-function/"""

aq_df = pd.read_csv('/content/tmp/aq/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv', parse_dates = [['year','month','day','hour']], date_parser = convert_to_date, keep_date_col=True)

aq_df

aq_df.info()

aq_df['month'] = pd.to_numeric(aq_df['month'])

print('Rows :', aq_df.shape[0])
print('Columns :', aq_df.shape[1])
print("\n Features: \n", aq_df.columns.tolist())
print("\n Missing Values: \n", aq_df.isnull().any())
print("\nUnique Values \n", aq_df.nunique())

aq_df.describe()

"""### **2.1 Make copy of data**"""

aq_df_non_indexed = aq_df.copy()

aq_df = aq_df.set_index('year_month_day_hour')

aq_df.index

aq_df.head()

"""### **2.2 Querying the data between dates**"""

aq_df.loc['2013-03-01':'2013-03-05']

aq_df.loc['2013':'2015']

pm_data = aq_df['PM2.5']
pm_data.head()

pm_data.tail()

"""### **2.3 Plotting the PM2.5 data**"""

pm_data.plot(grid=True)

"""### **2.4 Visualise the data only for year**"""

aq_df_2014 = aq_df.loc['2014']
pm_data_2014 = aq_df_2014['PM2.5']
pm_data_2014.plot(grid = True)

aq_df_2015 = aq_df.loc['2015']
pm_data_2015 = aq_df_2015['PM2.5']
pm_data_2015.plot(grid = True)

aq_df_2016 = aq_df.loc['2016']
pm_data_2016 = aq_df_2016['PM2.5']
pm_data_2016.plot(grid = True)

"""From above graphs, it is clear that there is seasonality in data.
PM2.5 is increasing from October to March and then decreasing.

### **2.5 Visualization with Plotly**
"""

import plotly.express as px
fig = px.line(aq_df_non_indexed, x='year_month_day_hour', y='PM2.5', title = 'PM2.5 with slider')

fig.update_xaxes(rangeslider_visible = True)
fig.show()

fig = px.line(aq_df_non_indexed, x='year_month_day_hour', y='PM2.5', title = 'PM2.5 with slider')

fig.update_xaxes(
    rangeslider_visible = True,
    rangeselector = dict(
        buttons = ([
            dict(count=1, label = '1y', step='year', stepmode = 'backward'),
            dict(count=2, label = '2y', step='year', stepmode = 'backward'),
            dict(count=3, label = '3y', step='year', stepmode = 'backward'),
            dict(step='all')
        ])
    )
)

fig.show()

"""### **2.6 Overlay different year datasets**"""

df_2014 = aq_df['2014'].reset_index()
df_2015 = aq_df['2015'].reset_index()
df_2016 = aq_df['2016'].reset_index()
df_2014['month_day_hour'] = df_2014.apply(lambda x:str(x['month'])+"-"+x['day'], axis=1)
df_2015['month_day_hour'] = df_2015.apply(lambda x:str(x['month'])+"-"+x['day'], axis=1)
df_2016['month_day_hour'] = df_2016.apply(lambda x:str(x['month'])+"-"+x['day'], axis=1)
plt.plot(df_2014['month_day_hour'], df_2014['PM2.5'])
plt.plot(df_2015['month_day_hour'], df_2015['PM2.5'])
plt.plot(df_2016['month_day_hour'], df_2016['PM2.5'])
plt.legend(['2014','2015','2016'])
plt.xlabel('Month')
plt.ylabel('PM2.5')
plt.title('Air quality plot for the year 2014,2015 and 2016')

aq_df['2014':'2016'][['month','PM2.5']].groupby('month').describe()

aq_df['2014':'2016'][['month','PM2.5','TEMP']].groupby('month').describe()

aq_df['2014':'2016'][['month','PM2.5','PRES']].groupby('month').describe()

aq_df['2014':'2017'][['month','PM2.5','TEMP','PRES']].groupby('month').agg({'PM2.5':['min','max'],'TEMP':['min','max'],'PRES':['min','max']})

aq_df_2014 = aq_df['2014']
pm_data_2014 = aq_df_2014[['PM2.5','TEMP','PRES']]
pm_data_2014.plot(subplots = True)

aq_df_2015 = aq_df['2015']
pm_data_2015 = aq_df_2015[['PM2.5','TEMP','PRES']]
pm_data_2015.plot(subplots = True)

aq_df_2016 = aq_df['2016']
pm_data_2016 = aq_df_2016[['PM2.5','TEMP','PRES']]
pm_data_2016.plot(subplots = True)

"""Refer : https://weather.com/en-IN/india/science/news/2018-10-30-why-do-pollution-levels-skyrocket-during-winter"""

aq_df[['PM2.5','PM10','TEMP','PRES']].hist()

aq_df[['PM2.5','TEMP','PRES']].plot(kind='density')

aq_df[['TEMP','PRES']].plot(kind='density')

"""# **3.0 Lag Plot**"""

pd.plotting.lag_plot(aq_df['TEMP'],lag=1)

pd.plotting.lag_plot(aq_df['TEMP'],lag=10)

pd.plotting.lag_plot(aq_df['TEMP'],lag=24)

pd.plotting.lag_plot(aq_df['TEMP'],lag=8640)   #one year--->>> Positive correlation

pd.plotting.lag_plot(aq_df['TEMP'],lag=4320)  #six months --->>> Negative correlation

pd.plotting.lag_plot(aq_df['TEMP'],lag=2150)   #3months   --->>> No correlation

multi_data = aq_df[['TEMP','PRES','DEWP','RAIN','PM2.5']]
multi_data.plot(subplots= True)

multi_data2 = aq_df[['SO2','NO2','O3','CO','PM2.5']]
multi_data2.plot(subplots= True)

aq_df['2014':'2015'][['PM2.5','O3','NO2']].plot(figsize=(15,8),linewidth=3,fontsize=15)
plt.xlabel('year_month_day_hour',fontsize = 15)

aq_df_2015['PM2.5']

aq_df_2015

aq_df.isnull().values.any()

aq_df.isnull().any()

aq_df.isnull().sum()

# Correlation between variables
g = sns.pairplot(aq_df[['SO2','NO2','O3','CO','PM2.5','PM10']])

aq_corr = aq_df[['SO2','NO2','O3','CO','PM2.5','PM10']].corr(method = 'pearson')
aq_corr

"""## **3.1 Generate heatmap to visualize correlation**"""

g = sns.heatmap(aq_corr, vmax=.6, center=0, square = True, linewidth = .5, cbar_kws={'shrink':.5}, annot = True, fmt = '.2f', cmap='coolwarm' )
g.figure.set_size_inches(10,10)

plt.show()

aq_df.groupby('wd').agg(median=('PM2.5','median'),mean=('PM2.5','mean'),max=('PM2.5','max'),min=('PM2.5','min')).reset_index()

# Drop the null values
aq_df_na = aq_df.copy()
aq_df_na = aq_df_na.dropna()

from pandas.plotting import autocorrelation_plot
autocorrelation_plot(aq_df_na['2014':'2016']['TEMP'])

pd.plotting.autocorrelation_plot(aq_df_na['2013':'2015']['TEMP'])

aq_df_na['TEMP'].resample('1m').mean()

autocorrelation_plot(aq_df_na['2014':'2016']['TEMP'].resample('1m').mean())

autocorrelation_plot(aq_df_na['2014':'2016']['PM2.5'].resample('1m').mean())

