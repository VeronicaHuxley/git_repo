#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import math
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import csv
#import pandas_profiling
import statsmodels.formula.api as sm


# # Correlations, OLS and Linear Regression Models: <br>The Influential Factors of Geographic Mobility in Mid-size Metro U.S.

# ## Overview 
# Cities around the U.S. are experiencing rapid changes in population, quality of life, happiness of their residents, and income inequality, due to a range of factors -- environmental changes, access to public transportation, business growth or decline, cost of living, taxes, welfare programs, quality of education, and many more. The correlation of some of these factors is clear; for example, it’s been well documented that cities with declining industries see related decreases in population as people pursue employment opportunities elsewhere. However, city growth or decline is a complex issue, one that cities, their leaders, and their residents have yet to explore in-depth.
# 
# ## Why does this problem matter?
# Government leaders have a clear stake in this issue -- a desire to create stable, thriving cities; an incentive to prevent a brain drain and continue to grow business and innovation in their cities; a need to effectively allocate funding in education and public programs that help their constituents be healthy and happy. The goal is to explore the factors that contribute to cities’ growth or decline and identify ways that leaders can improve their own cities (e.g. through additional investments in infrastructure, policy changes, etc).<br><br>
# 
# Using data from the US Census this analysis covers the incoming geographic mobility rates for 27 cities as well as the demographic of those moving on the assumption that the amount of people moving into cities is a good metric for a city’s growth.<br><br>
# 
# Austin, TX | Fort Worth, TX | Jacksonville, FL | Columbus, OH | Charlotte, NC | San Francisco, CA | Indianapolis, IN | Denver, CO | Seattle, WA | Denver, CO | Washington, D.C. | Boston, MA | El Paso, TX | Detroit, MI | Nashville, TN | Oklahoma City, OK | Portland, OR | Las Vegas, NV | Memphis, TN | Louisville, KY | Baltimore, MD | Milwaukee, WI | Albuquerque, NM | Tucson, AZ | Fresno, CA | Mesa, AZ | Sacramento, CA | Kansas City, MO
# 

# After further analysis, the cities with the most and least geographic mobility are the following:
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville 
# 
# 

# <b>Correlations:</b><br> 
#     1. Geo Mobility & Business Dynamics/Growth Top & Bottom 5 Cities<br> 
#     2. Geo Mobility & Individual Income Top & Bottom 5 Cities
#  
# <br>     
# <b>Ordinary Least Square Regression Model:</b><br>  
# 1. Individual Income<br> 
# 2. Household Welfare <br> 
# 3. Unemployment Rate<br> 
# 4. Income Inequality<br> 
# 5. Median Gross Rent to Income<br> 
# 6. Geographic Mobility <br> 
# 7. Educational Attainment <br> 
# 8. Business Growth & Dynamics<br> 
# <br> <br> 
# <b>Linear Regression Models:</b><br> 
# 1. Geographic Mobility <br> 
# 2. Business Growth & Dynamics<br> 
# 3. Unemployment Rate<br> 
# 4. Income Inequality <br> 
# 5. Median Gross Rent to Income<br> 
# 6. Household Welfare<br> 
# 7. Educational Attainment<br> 
# 
# <br> 
#     
#     

# ### Business Dynamics/Growth - Top & Bottom 5 Cities
# 

# In[ ]:


#Opening, reading, dropping column and changing 'percent_change' number to float in .csv
with open('data/business_dynamics.csv') as f:
    business_dynamics = pd.read_csv(f).drop(columns=['metro','firms', 'estab_change',])
    business_dynamics['business_percent_change'] = pd.to_numeric(business_dynamics['percent_change'],errors = 'coerce')
business_27 = business_dynamics[business_dynamics['year'] != 2010]
business_27


# In[ ]:


business_27.describe()


# In[ ]:


business_10 = business_27[(business_27.values  == 'Memphis')|(business_27.values  == 'Milwaukee')|(business_27.values  == 'Detroit')|(business_27.values  == 'Louisville')|(business_27.values  == 'Fresno')|(business_27.values  == 'Denver')|(business_27.values  == 'Boston')|(business_27.values  == 'Austin')|(business_27.values  == 'Seattle')|(business_27.values  == 'Washington')]
business_10


# In[ ]:


business_top_5 = business_27[(business_27.values  == 'Denver')|(business_27.values  == 'Boston')|(business_27.values  == 'Austin')|(business_27.values  == 'Seattle')|(business_27.values  == 'Washington')]
business_top_5


# In[ ]:


business_bottom_5 = business_27[(business_27.values  == 'Memphis')|(business_27.values  == 'Milwaukee')|(business_27.values  == 'Detroit')|(business_27.values  == 'Louisville')|(business_27.values  == 'Fresno')]
business_bottom_5


# In[ ]:


business_10['estab'].pct_change()


# ### Geographic Mobility - Top & Bottom 5

# Geographical Mobility based on US Census data from 2010-2019, including breakdowns by demographic characteristics and rates of inmigration, outmigration, and net migration. This is an important variable for comparing how geographic mobility has changed over time across the top 5 and bottom 5 ranking cities and its potential correlation.
# 
# <b>name:</b> City name.
# 
# <b>year:</b> Record year for which the data was gathered per year between 2010-2019.
# 
# <b>same_county:</b> Moved within the same county. Estimate population 1 year and over.
# 
# <b>diff_county:</b> Moved from a different county, same state. Estimate population 1 year and over.
# 
# <b>diff_state:</b> Moved from a different state. Estimate population 1 year and over.
# 
# <b>from_abroad</b>: Moved from abroad. Estimate population 1 year and over.
# 
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville 

# In[ ]:


#Read geographic mobility dataset, drop columns and create total mobility column
with open('data/geo_mobility.csv') as f:
    geo_mobility_27 = pd.read_csv(f).drop(columns=['city_state', 'geo_id']).sort_values(by='year', ascending=False)
    #geo_mobility_27['total_mobility_all'] = geo_mobility_27['same_county'] + geo_mobility_27['diff_county'] + geo_mobility_27['diff_state'] + geo_mobility_27['from_abroad']
    geo_mobility_27['total_mobility_outside'] = geo_mobility_27['diff_county'] + geo_mobility_27['diff_state'] + geo_mobility_27['from_abroad']
    #geo_mobility_15['geo_percent_change'] = geo_mobility_15['total_mobility_all'].pct_change()
    geo_mob_27 = geo_mobility_27#.groupby(['name])
geo_mob_27


# In[ ]:


geo_mob_10 = geo_mob_27[(geo_mob_27.values  == 'Memphis')|(geo_mob_27.values  == 'Milwaukee')|(geo_mob_27.values  == 'Detroit')|(geo_mob_27.values  == 'Louisville')|(geo_mob_27.values  == 'Fresno')|(geo_mob_27.values  == 'Denver')|(geo_mob_27.values  == 'Boston')|(geo_mob_27.values  == 'Austin')|(geo_mob_27.values  == 'Seattle')|(geo_mob_27.values  == 'Washington')]
geo_mob_10


# In[ ]:


#creating a separate df and dropping Louisvilee to compare to individual income as that dataset does not have Louisville
geo_mob_10_2 = geo_mob_10[geo_mob_10['name'] != 'Louisville']
geo_mob_10_2


# In[ ]:


geo_mob_top_5 = geo_mob_27[(geo_mob_27.values  == 'Denver')|(geo_mob_27.values  == 'Boston')|(geo_mob_27.values  == 'Austin')|(geo_mob_27.values  == 'Seattle')|(geo_mob_27.values  == 'Washington')]
geo_mob_top_5


# In[ ]:


geo_mob_bottom_5 = geo_mob_27[(geo_mob_27.values  == 'Memphis')|(geo_mob_27.values  == 'Milwaukee')|(geo_mob_27.values  == 'Detroit')|(geo_mob_27.values  == 'Louisville')|(geo_mob_27.values  == 'Fresno')]
geo_mob_bottom_5


# In[ ]:


#creating separate df EXCLUDING Louisville to merge with Individual Income df below (no Ind Income data available for Loiusville)
geo_mob_bottom_5_2 = geo_mob_27[(geo_mob_27.values  == 'Memphis')|(geo_mob_27.values  == 'Milwaukee')|(geo_mob_27.values  == 'Detroit')|(geo_mob_27.values  == 'Fresno')]
geo_mob_bottom_5_2


# ### Individual Income - Top 5 & Bottom 4

# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Except Louisville (Individual Income data not avialable for Louisville)

# In[ ]:


#Read geographic mobility dataset, drop columns and create total mobility column
with open('data/individual_income.csv') as f:
    individual_income = pd.read_csv(f).drop(columns=['city_state', 'total_est_mean_earnings', 'male_est_median_earnings', 'female_est_median_earnings', 'male_est_mean_fulltime_earnings', 'female_est_mean_fulltime_earnings'])#.sort_values(by='year', ascending=False)
    #individual_income['male_median_percent_change'] = individual_income['male_est_median_fulltime_earnings'].pct_change()
    #individual_income['female_median_percent_change'] = individual_income['female_est_median_fulltime_earnings'].pct_change()
    #individual_income['total_pop_income_percent_change'] = individual_income['total_est_pop_over16'].pct_change()
    #individual_income['total_pop_ind_income_median_percent_change'] = individual_income['total_est_median_earnings'].pct_change()
    ind_income_27 = individual_income
ind_income_27


# In[ ]:


ind_income_27.name.unique()


# In[ ]:


ind_income_10 = ind_income_27[(ind_income_27.values  == 'Memphis')|(ind_income_27.values  == 'Milwaukee')|(ind_income_27.values  == 'Detroit')|(ind_income_27.values  == 'Louisville')|(ind_income_27.values  == 'Fresno')|(ind_income_27.values  == 'Denver')|(ind_income_27.values  == 'Boston')|(ind_income_27.values  == 'Austin')|(ind_income_27.values  == 'Seattle')|(ind_income_27.values  == 'Washington')]
ind_income_10


# In[ ]:


ind_income_top_5 = ind_income_27[(ind_income_27.values  == 'Denver')|(ind_income_27.values  == 'Boston')|(ind_income_27.values  == 'Austin')|(ind_income_27.values  == 'Seattle')|(ind_income_27.values  == 'Washington')]
ind_income_top_5


# In[ ]:


ind_income_bottom_4 = ind_income_27[(ind_income_27.values  == 'Memphis')|(ind_income_27.values  == 'Milwaukee')|(ind_income_27.values  == 'Detroit')|(ind_income_27.values  == 'Louisville')|(ind_income_27.values  == 'Fresno')]
ind_income_bottom_4


# #### Plotly Box Plot of total estimated median of individual income
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#Plotly Box Plot of total estimated median of individual income - 2010-2019

fig = px.box(ind_income_top_5, x='name', y='total_est_median_earnings', points='all', # can be 'all', 'outliers', or False
             title="Box Plot of total estimated median of individual income of total population | Top 5 Cities - 2010-2019", hover_data=ind_income_top_5.columns,
             labels={col:col.replace('_', ' ') for col in ind_income_top_5.columns}) # remove underscore
fig.show()


# #### Plotly Box Plot of total estimated median of individual income
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Except Louisville (Individual Income data not avialable for Louisville)

# In[ ]:


#Plotly Box Plot total estimated median of individual income by year with outliers - 2010-2019

fig = px.box(ind_income_bottom_4, x='name', y='total_est_median_earnings', points='all', # can be 'all', 'outliers', or False
             title="Box Plot of total estimated median of individual income of total population | Bottom 4 Cities - 2010-2019", hover_data=ind_income_bottom_4.columns,
             labels={col:col.replace('_', ' ') for col in ind_income_bottom_4.columns}) # remove underscore
fig.show()


# # CORRELATIONS:<br> Geo Mobility & Business Dynamics/Growth  Top & Bottom 5

# 
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#Merging dataselts for top 5 and bottom 5 cities of geo mobility and business_dynamics datasets for visualization of possible correlations
mob_bgrowth_10 = pd.merge(business_10, geo_mob_10, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_bgrowth_10


# In[ ]:


mob_bgrowth_10[['business_percent_change','total_mobility_outside','total_year']].describe()


# #### Ordinary Least Squares regression trendline - Top 5 and Bottom 5 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#Plotly scatterplot Ordinary Least Squares regression trendline of TOP 5 and BOTTOM 5 cities
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_bgrowth_10, x='total_mobility_outside', y='business_percent_change', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_bgrowth_10.columns}) # removes underscore
fig.show()


# #### Pearson's Correlation of Geo Mobility & Business Dynamics - Top 5 and Bottom 5 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
mob_bgrowth_10.corr().style.background_gradient(cmap="Blues")


# In[ ]:


mob_bgrowth_10[['business_percent_change', 'total_mobility_outside']].corr()


# #### Spearman's Correlation of Geo Mobility & Business Dynamics - Top 5 and Bottom 5 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
mob_bgrowth_10.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


corrm = mob_bgrowth_10.corr()
corrm


# ### Merging Geo Mobility & Business Dynamics datasets - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#Merging datasets of TOP 5 cities for geo mobility and business_dynamics for visualization of possible correlations
mob_bgrowth_top_5 = pd.merge(business_top_5, geo_mob_top_5, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_bgrowth_top_5


# #### Ordinary Least Squares regression trendline - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#Plotly scatterplot of TOP 5 cities ONLY - Ordinary Least Squares regression trendline of business growth percent change by year for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_bgrowth_top_5, x='total_mobility_outside', y='business_percent_change', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_bgrowth_top_5.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Total Mobility %', yaxis_title = 'Business Dynamics % Change')
fig.show()


# In[ ]:


#Plotly scatterplot of TOP 5 cities ONLY - Ordinary Least Squares regression trendline of business growth percent change by year for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_bgrowth_top_5, x='total_mobility_outside', y='business_percent_change', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_bgrowth_top_5.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Total Mobility %', yaxis_title = 'Business Dynamics % Change')
fig.show()


# #### Pearson's Correlation of Geo Mobility & Business Dynamics - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
mob_bgrowth_top_5.corr().style.background_gradient(cmap="Blues")


# #### Spearman's Correlation of Geo Mobility & Business Dynamics - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
mob_bgrowth_top_5.corr('spearman').style.background_gradient(cmap="Blues")


# ### Merging Geo Mobility & Business Dynamics datasets - Bottom 5 cities only
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#Merging datasets of BOTTOM 5 cities for geo mobility and business_dynamics for visualization of possible correlations
mob_bgrowth_bottom_5 = pd.merge(business_bottom_5, geo_mob_bottom_5, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_bgrowth_bottom_5


# #### Ordinary Least Squares regression trendline of Geo Mobility & Business Dynamics - Bottom 5 cities only
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#Plotly scatterplot of BOTTOM 5 cities ONLY - Ordinary Least Squares regression trendline of Geo Mobility & Business Dynamics
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_bgrowth_bottom_5, x='total_mobility_outside', y='business_percent_change', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_bgrowth_bottom_5.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Bottom 5 Cities Total Mobility %', yaxis_title = 'Bottom 5 Cities Business Dynamics % Change')
fig.show()


# #### Pearson's Correlation of Geo Mobility & Business Dynamics - Bottom 5 cities only
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#business dynamics/growth % and geo mobility % change YoY using Pearson correlation coefficient to summarize its strength 
mob_bgrowth_bottom_5.corr().style.background_gradient(cmap="Blues")


# In[ ]:


mob_bgrowth_bottom_5[['business_percent_change', 'total_mobility_outside']].corr()


# #### Spearman's Correlation of Geo Mobility & Business Dynamics - Bottom 5 cities only
# ##### Bottom 5 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#business dynamics/growth % change YoY and geo mobility % change YoY using Spearman correlation coefficient
mob_bgrowth_bottom_5.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


corrm = mob_bgrowth_bottom_5.corr()
corrm


# # CORRELATIONS: <br> Geo Mobility & Individual Income

# 
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#Merging datasets of Top 5 and Bottom 5 cities for geo mobility and Individual Income for visualization of possible correlations
# Excluding Loiuville from df (No Ind Income data available)
mob_ind_income_10 = pd.merge(ind_income_10, geo_mob_10_2, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_ind_income_10


# #### Ordinary Least Squares regression trendline of  Geo Mobility & Individual Income - Top 5 and Bottom 4 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#Plotly scatterplot - Ordinary Least Squares regression trendline of TOP 5 and BOTTOM 5 cities
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_10, x='total_mobility_outside', y='total_est_median_earnings', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_10.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Top & Bottom 5 Cities Total Mobility %', yaxis_title = 'Top & Bottom 5 Cities Individual Income Median')
fig.show()


# In[ ]:


#Plotly scatterplot - Ordinary Least Squares regression trendline of TOP 5 and BOTTOM 5 cities
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_10, x='total_mobility_outside', y='total_est_pop_over16', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_10.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Top & Bottom 5 Cities Total Mobility %', yaxis_title = 'Top & Bottom 5 Cities Total Population Earnings')
fig.show()


# #### Pearson's Correlation of Geo Mobility & Individual Income - Top 5 and Bottom 4 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#geo mobility individual income using Pearson correlation coefficient to summarize its strength 
mob_ind_income_10.corr().style.background_gradient(cmap="Blues")


# In[ ]:


mob_ind_income_10[['total_est_median_earnings', 'total_mobility_outside', 'total_est_pop_over16']].corr()


# #### Spearman's Correlation of Geo Mobility & Individual Income - Top 5 and Bottom 4 cities
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#geo mobility and individual income using Spearman correlation coefficient
mob_ind_income_10.corr('spearman').style.background_gradient(cmap="Blues")


# ### Merging Geo Mobility & Individual Income datasets for correlation of Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#Merging datasets for correlation of Top 4 cities only for Geo Mobility & Individual Income for visualization of possible correlations
mob_ind_income_top_5 = pd.merge(ind_income_top_5, geo_mob_top_5, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_ind_income_top_5


# #### Ordinary Least Squares regression trendline of  Geo Mobility & Individual Income - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#Plotly scatterplot of TOP 5 cities ONLY - Ordinary Least Squares regression trendline
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_top_5, x='total_mobility_outside', y='total_est_median_earnings', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_top_5.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Top 5 Cities Total Mobility %', yaxis_title = 'Top 5 Cities Total Individual Income Median')
fig.show()


# In[ ]:


#Plotly scatterplot of TOP 5 cities ONLY - Ordinary Least Squares regression trendline
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_top_5, x='total_mobility_outside', y='total_est_pop_over16', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_top_5.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Top 5 Cities Total Mobility %', yaxis_title = 'Top 5 Cities Total Populatin Earnings')
fig.show()


# #### Pearson's Correlation of Geo Mobility & Individual Income - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#geo mobility individual income using Pearson correlation coefficient to summarize its strength 
mob_ind_income_top_5.corr().style.background_gradient(cmap="Blues")


# In[ ]:


mob_ind_income_top_5[['total_est_median_earnings', 'total_mobility_outside']].corr()


# #### Spearman's Correlation of Geo Mobility & Individual Income - Top 5 cities only
# ##### Top 5 cities: 
# Denver | Boston | Austin | Seattle | Washington, DC

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#geo mobility and individual income using Spearman's correlation coefficient
mob_ind_income_top_5.corr('spearman').style.background_gradient(cmap="Blues")


# ### Merging Geo Mobility & Individual Income datasets for correlation of Bottom 4 cities only
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#Merging datasets for correlation of bottom 4 cities for Geo Mobility & Individual Income 
#for visualization of possible correlations
#Excluding Louisville -- Individual Income data is not available
mob_ind_income_bottom_4 = pd.merge(ind_income_bottom_4, geo_mob_bottom_5_2, on=['name','year']).drop(columns=['same_county', 'diff_county', 'from_abroad'])
mob_ind_income_bottom_4


# #### Ordinary Least Squares regression trendline of Geo Mobility & Individual Income - Bottom 4 cities only
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#Plotly scatterplot of bottom 4 cities ONLY - Ordinary Least Squares regression trendline
#Excluding Louisville -- Individual Income data is not available
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_bottom_4, x='total_mobility_outside', y='total_est_median_earnings', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_bottom_4.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Bottom 4 Cities Total Mobility %', yaxis_title = 'Bottom 4 Cities Total Individual Income Median')

fig.show()


# In[ ]:


#Plotly scatterplot of bottom 4 cities ONLY - Ordinary Least Squares regression trendline
#Excluding Louisville -- Individual Income data is not available
#Hovering over the trendline will show the equation of the line and its R-squared value.

fig = px.scatter(mob_ind_income_bottom_4, x='total_mobility_outside', y='total_est_pop_over16', trendline='ols', color='year', hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in mob_ind_income_bottom_4.columns}) # removes underscore
fig.update_layout(xaxis_title = 'Bottom 4 Cities Total Mobility %', yaxis_title = 'Bottom 4 Cities Total Population Earnings')

fig.show()


# #### Pearson's Correlation of Geo Mobility & Individual Income - Bottom 5 cities only
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#correlation matrix calculation and visualization of possible linear relationship between
#geo mobility individual income using Pearson's correlation coefficient to summarize its strength 
##Excluding Louisville -- Individual Income data is not available
mob_ind_income_bottom_4.corr().style.background_gradient(cmap="Blues")


# In[ ]:


mob_ind_income_bottom_4[['total_est_pop_over16', 'total_mobility_outside']].corr()


# #### Spearman's Correlation of Geo Mobility & Individual Income - Bottom 4 cities only
# ##### Bottom 4 cities: 
# Memphis | Milwaukee | Detroit | Fresno | Louisville | [Louisville
# -- Individual Income data is not available for Louisville.]

# In[ ]:


#correlation matrix calculation and visualization of monotonic relationship between
#geo mobility and individual income using Spearman's correlation coefficient
#Excluding Louisville -- Individual Income data is not available
mob_ind_income_bottom_4.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


corrm = mob_ind_income_bottom_4.corr()
corrm


# In[ ]:


corrm['total_est_median_earnings'][corrm['total_mobility_outside'] > 0].sort_values(ascending = False)


# # Ordinary Least Square Regression Model

# In[ ]:


#Merging mobility and business dynamics
mobility_business = pd.merge(geo_mob_27, business_27, on=['name','year'])
mobility_business = mobility_business.drop(columns=['total_year', 'same_county', 'diff_county','estab', 'emp',
       'percent_change','diff_state', 'from_abroad',])
mobility_business


# In[ ]:


mobility_business_indincome = pd.merge(mobility_business, ind_income_27, on=['name','year']) 
mobility_business_indincome = mobility_business_indincome.drop(columns=['male_est_pop_over16', 'male_est_median_fulltime_earnings',
       'female_est_pop_over16', 'female_est_median_fulltime_earnings'])
mobility_business_indincome


# In[ ]:


mobility_business_indincome.name.unique()


# In[ ]:


mobility_business_indincome.columns


# In[ ]:


with open('data/welfare.csv') as f:
    welfare = pd.read_csv(f)#.drop(columns=['metro', 'firms', 'estab_change',])
welfare


# In[ ]:


mobility_business_indincome_welfare = pd.merge(mobility_business_indincome, welfare, on=['name','year'])
mobility_business_indincome_welfare = mobility_business_indincome_welfare.drop(columns=['estimate_total_households_with_social_security',
       'mean_social_security_income_usd',
       'estimate_total_households_with_retirement_income',
       'percent_estimate_total_households_with_retirement_income',
       'mean_retirement_income_usd', 'estimate_total_households_with_ssi',
       'percent_estimate_total_households_with_ssi', 'mean_ssi_income_usd',
       'estimate_total_households_with_cash_public_assistance',
       'percent_estimate_total_households_with_cash_public_assistance',
       'mean_cash_public_assistance_income_usd',
       'total_households_foodstamp_snap',])
mobility_business_indincome_welfare


# In[ ]:


mobility_business_indincome_welfare.columns


# In[ ]:


with open('data/geo_mobility_combined.csv') as f:
    mobility_combined = pd.read_csv(f)#.drop(columns=['metro', 'firms', 'estab_change',])
mobility_combined


# In[ ]:


total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income = pd.merge(mobility_business_indincome_welfare, mobility_combined, on=['name','year'])
total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income


# In[ ]:


total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income.columns


# In[ ]:


mobility_combined.columns


# In[ ]:


#Opening, reading, dropping column and changing 'percent_change' number to float in .csv
with open('data/geo_mobility_ed_attainment.csv') as f:
    geo_mobility_ed_attainment = pd.read_csv(f).drop(columns=['move_same_county', 'city_state', 'move_total_year','move_diff_county',
       'move_diff_state', 'move_from_abroad','diff_county_ed_attn_pop_25up',
       'diff_county_ed_attn_less_than_high', 'diff_county_ed_attn_high',
       'diff_county_ed_attn_some coll_assoc', 'diff_county_ed_attn_bach',
       'diff_county_ed_attn_grad', 'diff_state_ed_attn_pop_25up',
       'diff_state_ed_attn_less_than_high', 'diff_state_ed_attn_high',
       'diff_state_ed_attn_some_coll_assoc', 'diff_state_ed_attn_bach',
       'diff_state_ed_attn_grad', 'from_abroad_ed_attn_pop_25up',
       'from_abroad_ed_attn_less_than_high', 'from_abroad_ed_attn_high',
       'from_abroad_ed_some_coll_assoc', 'from_abroad_ed_bach',
       'from_abroad_ed_grad'])
    #geo_mobility_ed_attainment['__'] = pd.to_numeric(business_dynamics['percent_change'],errors = 'coerce')
geo_mob_ed_attn = geo_mobility_ed_attainment
geo_mob_ed_attn


# In[ ]:


geo_mob_ed_attn.columns


# Datasets included below: business dynamics, business dynamics, individual income, welfare, unemployment_rate, income_ineq, mediangross_rent_income and educational attainment

# In[ ]:


#datasets: business dynamics, business dynamics, individual income, welfare, unemployment_rate, income_ineq, mediangross_rent_income and educational attainment
mobility_all = pd.merge(total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income, geo_mob_ed_attn, on=['name','year'])
mobility_all


# # Linear Regression Models
# ### Mobility Analysis  <br> 

# In[ ]:


formula1 = 'total_mobility_outside ~ business_percent_change + total_est_median_earnings'
model1 = sm.ols(formula = formula1, data = mobility_business_indincome)
fitted1 = model1.fit()
print(fitted1.summary())


# In[ ]:


formula2 = 'total_mobility_outside ~ business_percent_change + total_est_median_earnings + percent_estimate_total_households_with_social_security + percent_households_foodstamp_snap'
model2 = sm.ols(formula = formula2, data = total_est_median_earnings_welfare)
fitted2 = model2.fit()
print(fitted2.summary())


# In[ ]:


formula3 = 'total_mobility_outside ~ business_percent_change + total_est_median_earnings + unemployment_rate + income_ineq + mediangross_rent_income + percent_estimate_total_households_with_social_security + percent_households_foodstamp_snap'
model3 = sm.ols(formula = formula3, data = total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income)
fitted3 = model3.fit()
print(fitted3.summary())


# In[ ]:


formula4 = 'total_mobility_outside ~ business_percent_change + unemployment_rate + income_ineq + mediangross_rent_income + percent_households_foodstamp_snap'
model4 = sm.ols(formula = formula4, data = total_est_median_earnings_welfare_unemployment_rate_income_ineq_mediangross_rent_income)
fitted4 = model4.fit()
print(fitted4.summary())


# In[ ]:


formula5 = 'total_mobility_outside ~ business_percent_change + unemployment_rate + income_ineq + mediangross_rent_income + percent_households_foodstamp_snap + total_ed_attn_pop_25up'
model5 = sm.ols(formula = formula5, data = mobility_all)
fitted5 = model5.fit()
print(fitted5.summary())


# ## <b>Model 4 is the best fit based on the regression models above:</b> <br>
# #### total_mobility <br>
# 1.business_percent_change <br> 2.unemployment_rate <br> 3.income_ineq <br> 4.mediangross_rent_income <br> 
# 5.percent_households_foodstamp_snap' <br>6. mediangross_rent_income <br><br>
# 77% (R^2 value) of the variation in mobility can be explained by the variables in our model.
# 

# In[ ]:


geo_mob_ed_attn.info()


# In[ ]:


mobility_ed_attn_business = pd.merge(geo_mob_ed_attn, business_dynamics, on=['name','year']).drop(columns=['estab', 'emp', 'percent_change'])
mobility_ed_attn_business


# In[ ]:


mobility_all_v2 = pd.merge(mobility_all_v1, business_27, on=['name','year'])#.drop(columns=['same_county', 'diff_county', 'from_abroad'])
mobility_all_v2


# In[ ]:


mobility_ed_attn_business.to_csv('data/mobility_ed_attn_business.csv', index=False)


# In[ ]:


ind_income_27.to_csv('data/ind_income_27.csv', index=False)


# This project is still being developed. The final report will be published soon.

# Author - Veronica Huxley
