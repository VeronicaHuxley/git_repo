#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import csv
import pandas_profiling
import sweetviz


# # In-depth Exploratory Data Analysis of <br>The Influential Factors of Geographic Mobility in Mid-size Metro U.S.

# # One-Dimensional: Business Dynamics/Growth - Top & Bottom 5 Cities

# In[ ]:


#Opening, reading, dropping column and changing 'percent_change' number to float in .csv
with open('data/business_dynamics.csv') as f:
    business_dynamics = pd.read_csv(f).drop(columns=['metro', 'firms', 'estab_change',])
    business_dynamics['percent_change'] = pd.to_numeric(business_dynamics['percent_change'],errors = 'coerce')
    #business_dynamics_15['bus_percent_change'] = business_dynamics_15['percent_change']
    #business_dynamics_15['bus_percent_change'] = business_dynamics_15['estab'].pct_change()
    #business_dynamics_15['estab_percent_change'] = business_dynamics_15['estab'].pct_change()
    #business_dynamics_15['emp_percent_change'] = business_dynamics_15['emp'].pct_change()
    #business_dynamics_15['year'] = pd.to_datetime(business_dynamics_15['year'], format='%Y')
    business_10 = business_dynamics#.sort_values(by=['name', 'year'], ascending=False)
business_10


# In[ ]:


business_10.dtypes


# In[ ]:


business_10.describe()


# In[ ]:


business_10[['estab', 'emp']].corr()


# In[ ]:


#creating a separate df and dropping 2010 to compare percent change YoY
business_10 = business_10[business_10['year'] != 2010]
business_10


# In[ ]:


business_top = business_10[(business_10.values  == 'Denver')|(business_10.values  == 'Boston')|(business_10.values  == 'Austin')|(business_10.values  == 'Portland')|(business_10.values  == 'Oklahoma City')]
business_top


# In[ ]:


#Plotly line plot of Business Growth % change by Year Top & Bottom 5 Cities - 2010-2019

fig = px.line(business_15, x='year', y='percent_change', color='name', 
              title='Line Plot of Business Growth % change YoY Top & Bottom 5 Cities - 2010-2019',
              labels={col:col.replace('_', ' ') for col in business_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar plot of Business Growth % change YoY Top & Bottom 5 Cities- 2010-2019

fig = px.bar(business_15, y='name', x='percent_change', color='year', 
             title='Bar Plot of Business Growth % change YoY Top & Bottom 5 Cities- 2010-2019',
             labels={col:col.replace('_', ' ') for col in business_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of Business Growth % change YoY Top & Bottom 5 Cities- 2010-2019

fig = px.bar(business_15, y='year', x='name', color='percent_change', 
             title='Bar Plot of Business Growth % change YoY Top & Bottom 5 Cities - 2010-2019',
             labels={col:col.replace('_', ' ') for col in business_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of Business Growth % change YoY Top & Bottom 5 Cities- 2010-2019

fig = px.bar(business_15, y='percent_change', x='year', color='name', 
             title='Bar graph of Business Growth % change YoY - Top & Bottom 5 Cities - 2010-2019',
             labels={col:col.replace('_', ' ') for col in business_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatter plot of Business Growth % change YoY Top & Bottom 5 Cities- 2010-2019

fig = px.scatter(business_15, x='year', y='percent_change', 
                 color='name', symbol='name', #marginal_y="rug", 
                 title='Scatter Plot of Business Growth % change YoY Top & Bottom 5 Cities - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in business_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of business growth percent change by year for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(business_15, x='year', y='percent_change', trendline='ols', hover_data=['percent_change','name'],
                labels={col:col.replace('_', ' ') for col in business_15.columns}) # removes underscore
fig.show()


# In[ ]:


business_15['estab'].pct_change()


# # One-Dimensional: Unemployment - Top & Bottom 5 Cities

# In[ ]:


#Read unemployment dataset, drop columns 
with open('data/unemployment_15.csv') as f:
    unemployment_15 = pd.read_csv(f).drop(columns=['city_state']).sort_values(by='unemployment_rate', ascending=False)
    unemployment_15['unemp_percent_change'] = unemployment_15['unemployment_rate'].pct_change()
    unemp_15 = unemployment_15
unemp_15


# In[ ]:


#creating a separate df and dropping 2010 to compare percent change YoY
unemp_15_1 = unemp_15[unemp_15['year'] != 2010]


# In[ ]:


#Plotly bar graph of unemployment rate by year for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(unemp_15, y='unemployment_rate', x='year', color='name', 
             title='Bar Plot of unemployment rate by year for top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in unemp_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of unemployment percent change by year for top and bottom 5 - 2011-2019. Estimate population 1 year and over
#using unemp_15_1, a separate df and dropping 2010 to compare percent change YoY
fig = px.bar(unemp_15_1, y='unemp_percent_change', x='year', color='name', 
             title='Bar Plot of unemployment % change YoY for top and bottom 5 - 2011-2019',
             labels={col:col.replace('_', ' ') for col in unemp_15_1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of unemployment rate by year for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(unemp_15, y='name', x='unemployment_rate', color='year', 
             title='Bar graph of of unemployment rate top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in unemp_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of unemployment % change by year for top and bottom 5 - 2011-2019. Estimate population 1 year and over
#using unemp_15_1, a separate df and dropping 2010 to compare percent change YoY

fig = px.bar(unemp_15_1, y='name', x='unemp_percent_change', color='year', 
             title='Bar Plot of of unemployment % change top and bottom 5 - 2011-2019',
             labels={col:col.replace('_', ' ') for col in unemp_15_1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of unemployment rate by year for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.line(unemp_15, x='year', y='unemployment_rate', color='name', 
              title='Line Plot of unemployment rate top and bottom 5 - 2010-2019',
              labels={col:col.replace('_', ' ') for col in unemp_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of unemployment % change by year for top and bottom 5 - 2011-2019. Estimate population 1 year and over
#using unemp_15_1, a separate df and dropping 2010 to compare percent change YoY

fig = px.line(unemp_15_1, x='year', y='unemp_percent_change', color='name', 
              title='Line Plot of unemployment % change top and bottom 5 - 2011-2019',
              labels={col:col.replace('_', ' ') for col in unemp_15_1.columns}) # remove underscore
fig.show()


# # One-Dimensional: Geographic Mobility - Top & Bottom 5

# Geographical Mobility based on US Census data from 2010-2019, including breakdowns by demographic characteristics and rates of inmigration, outmigration, and net migration. This is an important variable for comparing how geographic mobility has changed over time across the top 5 and bottom 5 ranking cities and its potential correlation.
# 
# name: City name.
# 
# year: Record year for which the data was gathered per year between 2010-2019.
# 
# same_county: Moved within the same county. Estimate population 1 year and over.
# 
# diff_county: Moved from a different county, same state. Estimate population 1 year and over.
# 
# diff_state: Moved from a different state. Estimate population 1 year and over.
# 
# from_abroad: Moved from abroad. Estimate population 1 year and over.

# In[ ]:


#Read geographic mobility dataset, drop columns and create total mobility column
with open('data/geo_mobility_15.csv') as f:
    geo_mobility_15 = pd.read_csv(f).drop(columns=['city_state']).sort_values(by='year', ascending=False)
    #geo_mobility_15['total_mobility_all'] = geo_mobility_15['same_county'] + geo_mobility_15['diff_county'] + geo_mobility_15['diff_state']+geo_mobility_15['from_abroad']
    geo_mobility_15['total_mobility_outside'] = geo_mobility_15['diff_county'] + geo_mobility_15['diff_state']+geo_mobility_15['from_abroad']
    #geo_mobility_15['geo_percent_change'] = geo_mobility_15['total_mobility_all'].pct_change()
    geo_mob_15 = geo_mobility_15#.groupby(['name'])
geo_mob_15


# In[ ]:


#creating a separate df and dropping Louisvilee to compare to individual income as that dataset does not have Louisville
#geo_mob_15_2 = geo_mob_15[geo_mob_15['name'] != 'Louisville']
#geo_mob_15_2


# In[ ]:


geo_mob_15.info()


# In[ ]:


#Plotly Line plot of Total Mobility (including same county) by Year for top and bottom 5 - 2010-2019. Estimate population 1 year and over


fig = px.line(geo_mob_15, x='year', y='total_mobility_outside', color='name', 
              title="Line Plot of percent of Total Mobility by Year for top and bottom 5 - 2010-2019",
              labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of unemployment percent change by year for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(geo_mob_15, y='geo_percent_change', x='year', color='name', 
             title='Bar Plot of geo mobility % change YoY for top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of unemployment percent change by year for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(geo_mob_15, y='geo_percent_change', x='name', color='year', 
             title='Bar Plot of geo mobility % change YoY for top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of geo mobility percent change YoY for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(geo_mob_15, y='name', x='geo_percent_change', color='year', 
             title='Bar Plot of geo mobility % change YoY for top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of geo mobility percent change YoY for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.bar(geo_mob_15, y='name', x='total_mobility_all', color='year', 
             title='Bar Plot of total mobility for top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of geo mobility % change YoY for top and bottom 5 - 2010-2019. Estimate population 1 year and over

fig = px.line(geo_mob_15, x='year', y='geo_percent_change', color='name', 
              title='Line Plot of geo mobility % change YoY for top & bottom 5 - 2010-2019',
              labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Box Plot of percentage of Total Mobility by year with outliers - 2010-2019

fig = px.box(geo_mob_15, x='year', y='total_mobility_all', points='all', # can be 'all', 'outliers', or False
             title="Box Plot of % Total Mobility by year with outliers - 2010-2019", hover_data=geo_mob_15.columns,
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Box Plot of Geo Mobility % change YoY by year with outliers - 2010-2019

fig = px.box(geo_mob_15, x='year', y='geo_percent_change', points='all', #color='name', # can be 'all', 'outliers', or False
             title="Box Plot of Geo Mobility % change YoY with outliers - 2010-2019", hover_data=geo_mob_15.columns,
             labels={col:col.replace('_', ' ') for col in geo_mob_15.columns}) # remove underscore
fig.show()


# # One-Dimensional: Individual Income - Top & Bottom 5

# In[ ]:


#Read geographic mobility dataset, drop columns and create total mobility column
with open('data/individual_income_14.csv') as f:
    individual_income_14 = pd.read_csv(f).drop(columns=['city_state', 'total_est_mean_earnings','male_est_median_earnings', 'female_est_median_earnings', 'male_est_mean_fulltime_earnings', 'female_est_mean_fulltime_earnings']).sort_values(by='year', ascending=False)
    individual_income_14['male_median_percent_change'] = individual_income_14['male_est_median_fulltime_earnings'].pct_change()
    individual_income_14['female_median_percent_change'] = individual_income_14['female_est_median_fulltime_earnings'].pct_change()
    individual_income_14['total_pop_income_percent_change'] = individual_income_14['total_est_pop_over16'].pct_change()
    individual_income_14['total_pop_ind_income_median_percent_change'] = individual_income_14['total_est_median_earnings'].pct_change()
    ind_income_14 = individual_income_14
ind_income_14


# In[ ]:


ind_income_14.info()


# In[ ]:


#Plotly Line plot of total estimated median of individual income of total population for top and bottom 5

fig = px.line(ind_income_14, x='year', y='total_est_median_earnings', color='name', 
              title="Line Plot of total estimated median of individual income of total population - top & bottom 5 - 2010-2019",
              labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of % change Y0Y of total estimated median of individual income of total population for top and bottom 5


fig = px.line(ind_income_14, x='year', y='total_pop_income_percent_change', color='name', 
              title="Line Plot of  % change Y0Y of total estimated median of individual income of total population - top & bottom 5 - 2010-2019",
              labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of median % change of individual income of total population for top and bottom 5


fig = px.line(ind_income_14, x='year', y='total_pop_ind_income_median_percent_change', color='name', 
              title="Line Plot of median % change of individual income of total population for top & bottom 5 - 2010-2019",
              labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of estimated median of individual income of total population for top and bottom 5

fig = px.bar(ind_income_14, y='total_est_median_earnings', x='year', color='name', 
             title='Bar Plot of estimated median of individual income of total population - top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of estimated median of individual income of total population for top and bottom 5

fig = px.bar(ind_income_14, y='total_est_median_earnings', x='name', color='year', 
             title='Bar Plot of estimated median of individual income of total population - top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of estimated individual income of total population - top & bottom 5 - 2010-2019

fig = px.bar(ind_income_14, y='total_est_pop_over16', x='name', color='year', 
             title='Bar Plot of estimated median of individual income of total population - top & bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of of individual income % change YoY of total population - top and bottom 5 - 2010-2019

fig = px.bar(ind_income_14, y='total_pop_income_percent_change', x='year', color='name', 
             title='Bar Plot of individual income % change YoY of total population - top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph of of individual income % change YoY of total population - top and bottom 5 - 2010-2019

fig = px.bar(ind_income_14, y='total_pop_income_percent_change', x='name', color='year', 
             title='Bar Plot of individual income % change YoY of total population - top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph - est. median of individual income % change YoY of total population - top and bottom 5 - 2010-2019

fig = px.bar(ind_income_14, y='total_pop_ind_income_median_percent_change', x='year', color='name', 
             title='Bar Plot of est. median of individual income % change YoY of total population - top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly bar graph - est. median of individual income % change YoY of total population - top and bottom 5 - 2010-2019

fig = px.bar(ind_income_14, y='total_pop_ind_income_median_percent_change', x='name', color='year', 
             title='Bar Plot of est. median of individual income % change YoY of total population - top and bottom 5 - 2010-2019',
             labels={col:col.replace('_', ' ') for col in ind_income_14.columns}) # remove underscore
fig.show()


# # CORRELATION: Business Dynamics/Growth & Unemployment
# # Top & Bottom 5

# In[ ]:


#Merge business_dynamics and unemployment datasets for visualization of possible correlations
bgrowth_unemp_15 = pd.merge(business_15, unemp_15, on=['name','year'])
bgrowth_unemp_15


# In[ ]:


bgrowth_unemp_15.info()


# In[ ]:


bgrowth_unemp_15[['bus_percent_change','unemp_percent_change','unemployment_rate']].describe()


# In[ ]:


bgrowth_unemp_15.corr()['bus_percent_change'].to_frame().sort_values('bus_percent_change')


# In[ ]:


bgrowth_unemp_15[['unemp_percent_change', 'bus_percent_change']].corr()


# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and unemployment % change YoY using Spearman correlation coefficient
bgrowth_unemp_15.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and and unemployment % change YoY using using Pearson correlation coefficient to summarize its strength 
bgrowth_unemp_15.corr().style.background_gradient(cmap="Blues")


# In[ ]:


corrm = bgrowth_unemp_15.corr()
corrm


# In[ ]:


corrm['bus_percent_change'][corrm['unemp_percent_change'] > 0].sort_values(ascending = False)


# In[ ]:


corrm = bgrowth_unemp_15_top.corr()
corrm


# # CORRELATION: Business Dynamics/Growth & Geo Mobility - Top & Bottom 5

# In[ ]:


#Merge business_dynamics and geographic mobility datasets for visualization of possible correlations
bgrowth_geo_15 = pd.merge(business_15, geo_mob_15, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
bgrowth_geo_15


# In[ ]:


bgrowth_geo_15.info()


# In[ ]:


bgrowth_geo_15[['bus_percent_change','geo_percent_change','total_year']].describe()


# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
bgrowth_geo_15.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
bgrowth_geo_15.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


corrm = bgrowth_geo_15.corr()
corrm


# In[ ]:


bgrowth_geo_15[['geo_percent_change', 'bus_percent_change']].corr()


# In[ ]:


bgrowth_geo_15_top = bgrowth_geo_15[(bgrowth_geo_15.values  == 'Tuscon')|(bgrowth_geo_15.values  == 'Austin')|(bgrowth_geo_15.values  == 'Seattle')|(bgrowth_geo_15.values  == 'Columbus')|(bgrowth_geo_15.values  == 'Denver')]
bgrowth_geo_15_top


# In[ ]:


#Top 5 cities ONLY Pearson's correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
bgrowth_geo_15_top.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#Top 5 cities ONLY Spearman's correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
bgrowth_geo_15_top.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


bgrowth_geo_15_bottom = bgrowth_geo_15[(bgrowth_geo_15.values  == 'San Francisco')|(bgrowth_geo_15.values  == 'Louisville')|(bgrowth_geo_15.values  == 'Detroit')|(bgrowth_geo_15.values  == 'El Paso')|(bgrowth_geo_15.values  == 'Indianapolis')]
bgrowth_geo_15_bottom


# In[ ]:


#Bottom 5 cities ONLY Pearson's correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
bgrowth_geo_15_bottom.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#Bottom 5 cities ONLY Spearman's correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
bgrowth_geo_15_bottom.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) 
#for each city in comparison to business percentage change of business growth per year.
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(bgrowth_geo_15, x='total_mobility_all', y='bus_percent_change', trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (including same county) & business % change by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in bgrowth_geo_15.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Bar graph of total mobility (including same county) for each city per year in comparison to percentage change of business growth per year.

fig = px.bar(bgrowth_geomob2, x='total_mobility_all', y='percent_change', color='name', 
             title="Bar graph of total mobility (including same county) per year in comparison to % change of business growth per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in bgrowth_geomob2.columns}) # remove underscore
fig.show()


# # CORRELATION: Business Dynamics/Growth & Individual Income - Top & Bottom 5

# In[ ]:


#Merge business_dynamics and individual income datasets for visualization of possible correlations
bgrowth_ind_income_15 = pd.merge(business_15, ind_income_14, on=['name','year'])
bgrowth_ind_income_15


# In[ ]:


bgrowth_ind_income_15.info()


# In[ ]:


bgrowth_ind_income_15[['total_pop_income_percent_change', 'bus_percent_change']].describe()


# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and % change YoY of individual income for total pop using Spearman correlation coefficient
bgrowth_ind_income_15.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % change YoY and % change YoY of individual income for total pop using Spearman correlation coefficient
bgrowth_ind_income_15.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#corrm = bgrowth_ind_income_15.corr()
#corrm


# In[ ]:


bgrowth_ind_income_15[['total_pop_ind_income_median_percent_change', 'bus_percent_change', 'emp_percent_change',]].corr()


# In[ ]:


pos_cor = corrm['total_pop_ind_income_median_percent_change'] >0
corrm['total_pop_ind_income_median_percent_change'][pos_cor].sort_values(ascending = False).to_frame()


# In[ ]:


neg_cor = corrm['total_pop_ind_income_median_percent_change'] <0
corrm['total_pop_ind_income_median_percent_change'][neg_cor].sort_values(ascending = True).to_frame()


# # CORRELATION: Geographic Mobility & Individual Income - Top & Bottom 5

# In[ ]:


#Merge business_dynamics and individual income datasets for visualization of possible correlations
geo_ind_income_14 = pd.merge(geo_mob_15, ind_income_14, on=['name','year'])#.sort_values(by='total_mobility_all')
geo_ind_income_14


# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % change YoY and % change YoY of individual income for total pop using Spearman correlation coefficient
geo_ind_income_14.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and % change YoY of individual income for total pop using Spearman correlation coefficient
geo_ind_income_14.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


geo_ind_income_14[['total_mobility_all', 'total_mobility_outside', 'geo_percent_change', 'total_est_pop_over16', 'total_est_median_earnings', 'total_pop_income_percent_change']].corr()


# In[ ]:


geo_ind_income_14_top = geo_ind_income_14[(geo_ind_income_14.values  == 'Tucson')|(geo_ind_income_14.values  == 'Austin')|(geo_ind_income_14.values  == 'Seattle')|(geo_ind_income_14.values  == 'Columbus')|(geo_ind_income_14.values  == 'Denver')]
geo_ind_income_14_top


# In[ ]:


geo_ind_income_14_top.corr().style.background_gradient(cmap="Blues")


# In[ ]:


geo_ind_income_14_top.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


geo_ind_income_14_bottom = geo_ind_income_14[(geo_ind_income_14.values  == 'San Francisco')|(geo_ind_income_14.values  == 'Louisville')|(geo_ind_income_14.values  == 'Detroit')|(geo_ind_income_14.values  == 'El Paso')|(geo_ind_income_14.values  == 'Indianapolis')]
geo_ind_income_14_bottom


# In[ ]:


geo_ind_income_14_bottom.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


geo_ind_income_14_bottom.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) 
#for each city in comparison to business percentage change of business growth per year.
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(geo_ind_income_14, x='total_mobility_all', y='total_pop_income_percent_change', trendline="ols", 
                 title="Scatterplot of OLS trendline of total mobility (including same county) & individual income - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in geo_ind_income_14.columns}) # remove underscore
fig.show()


# Please refer to notebook 3 for further analysis, correlations, OLS and linear regression models.

# Author - Veronica Huxley 
