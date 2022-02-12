#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn
import plotly.express as px
import plotly.graph_objects as go
import csv
import pandas_profiling
import sweetviz
from matplotlib.ticker import StrMethodFormatter


# # Preliminary Exploratory Data Analysis of <br>The Influential Factors of Geographic Mobility in Mid-size Metro U.S.

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

# ## One-Dimensional Distribution: Business Dynamics

# The Business Dynamics Statistics includes measures of openings and closings of businesses, startups, job creation and destruction in addition to several other dynamics. The analysis of this data will provide insight on the growth or decline of each city’s economy throughout time. Tracking changes will also enable visualization of the dynamics underlying aggregate factors of a thriving city. 
# <br>
# <b>name:</b> City name.
# 
# <b>estab:</b> A single physical location at which business is conducted or services or industrial operations are performed. It is not necessarily identical with a company or enterprise, which may consist of one or more establishments. When two or more activities are carried on at a single location under a single ownership, all activities generally are grouped together as a single establishment. The entire establishment is classified on the basis of its major activity and all data are included in that classification. Establishment counts represent the number of locations with paid employees any time during the year.
# 
# <b>firms:</b> A firm is a business organization consisting of one or more domestic establishments in the same geographic area and industry that were specified under common ownership or control. The firm and the establishment are the same for single-establishment firms. For each multi-establishment firm, establishments in the same industry within a geographic area will be counted as one firm; the firm employment and annual payroll are summed from the associated establishments.
# 
# <b>emp:</b> Paid employment consists of full- and part-time employees, including salaried officers and
# executives of corporations, who are on the payroll in the pay period including March 12. Included
# are employees on paid sick leave, holidays, and vacations.
# 
# <b>estab_change:</b> The difference in number of active establishments from the previous year.
# 
# <b>percent_change:</b> The change percentage of business establishments year over year.

# In[2]:


with open('data/business_dynamics.csv') as f:
    business_dynamics = pd.read_csv(f).drop(columns=['metro']) #.sort_values(by='year', ascending=False)


# In[ ]:


#creating pandas-profiling html analytics report for business_dynamics
df = pd.read_csv('data/business_dynamics.csv')
pandas_profiling.ProfileReport(df)


# In[ ]:


#Changing data type for 'percent_change' from object to float
business_dynamics['percent_change'] = pd.to_numeric(business_dynamics['percent_change'],errors = 'coerce')


# In[ ]:


business_dynamics['name'].drop_duplicates()


# In[ ]:


business_dynamics_hist = business_dynamics['percent_change'].plot.hist()
business_dynamics_hist.set_title("% of Establishments Growth, 2010-2019") # Adding title
business_dynamics_hist.set_xlabel('% of Establishments Growth')
plt.plot()


# In[ ]:


#Seaborn bar graph of number of establishments per city by year

business_dynamics_bar = sns.FacetGrid(business_dynamics, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
business_dynamics_bar.map_dataframe(sns.barplot,x='year',y= 'percent_change').set(xlabel='Year', 
                                                        ylabel='% of Establishments Growth YoY')

    


# In[ ]:


#Seaborn line graph of number of establishments per city by year

business_dynamics_line = sns.FacetGrid(business_dynamics, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
business_dynamics_line.map_dataframe(sns.lineplot,x='year',y= 
                                          'percent_change').set(xlabel='Year', ylabel='% of Establishments Growth YoY')


# In[ ]:


sns.relplot(x='year', y='percent_change', hue='name',kind='line',data=business_dynamics)


# In[ ]:


sns.regplot(x='year', y='percent_change',data=business_dynamics,fit_reg=True)


# In[ ]:


#Plotly bar plot of Business Growth % by Year - 2010-2019

df1 = business_dynamics.reset_index()

fig = px.bar(df1, y='percent_change', x="year", color='name', 
             title="Bar Plot of Business Growth % by Year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly line plot of Business Growth % by Year - 2010-2019

df2 = business_dynamics.reset_index()
fig = px.line(df2, x="year", y='percent_change', color='name', 
              title="Line Plot of Business Growth % by Year - 2010-2019",
              labels={col:col.replace('_', ' ') for col in df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatter plot of Business Growth % by Year - 2010-2019

df3 = business_dynamics.reset_index()
fig = px.scatter(df3, x="year", y='percent_change', 
                 color='name', symbol='name', #marginal_y="rug", 
                 title="Scatter Plot of Business Growth % by Year - 2010-2019",
                 labels={col:col.replace('_', ' ') for col in df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly histogram of Business Growth % by Year - 2010-2019

df4 = business_dynamics.reset_index()
fig = px.histogram(df4, x="year", y='percent_change', color='name', 
                title="Histogram of Business Growth % Change by Year - 2010-2019", 
                barmode = 'group', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['estab_change'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'sum', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                #facet_col = 'name', facet_col_wrap=5, facet_row_spacing=0.076923,
                labels={col:col.replace('_', ' ') for col in df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly scatter matrix of Business Growth % by Year - 2010-2019

df5 = business_dynamics.reset_index()
fig = px.scatter_matrix(df5, title="Scatter Matrix of Business Growth % - 2010-2019",)
fig.show()


# In[ ]:


#Plotly scatter matrix of Business Growth % by Year - 2010-2019

df5 = business_dynamics.reset_index()
fig = px.scatter_matrix(df5, dimensions=["percent_change", "year"],
    color="name", title="Scatter Matrix of Business Growth by Year and Percent Change",
    labels={col:col.replace('_', ' ') for col in df5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly violin plot of Business Growth % by Year - 2010-2019

df6 = business_dynamics.reset_index()
fig = px.violin(df6, y="year", x='percent_change', box=True, color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Business Growth % per City by Year - 2010-2019", hover_data=df6.columns,
                labels={col:col.replace('_', ' ') for col in df6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly violin plot of Business Growth % by Year - 2010-2019

df7 = business_dynamics.reset_index()
fig = px.violin(df7, y="name", x='percent_change', box=True, color='name',# draw box plot inside the violin
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Business Growth Percent Change per City - 2010-2019", hover_data=df7.columns,
    labels={col:col.replace('_', ' ') for col in df7.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly violin plot of Business Growth % by Year - 2010-2019

df8 = business_dynamics.reset_index()
fig = px.violin(df8, y="percent_change", x='year', box=True, color='year',# draw box plot inside the violin
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Business Growth % Change by Year - 2010-2019", hover_data=['name'],
                labels={col:col.replace('_', ' ') for col in df8.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly box plot of Business Growth % by Year - 2010-2019 with outliers

df9 = business_dynamics.reset_index()
fig = px.box(df9, x="year", y="percent_change", points='outliers', # can be 'all', 'outliers', or False
             title="Box Plot of Business Growth % Change by year with outliers - 2010-2019", hover_data=df9.columns,
             labels={col:col.replace('_', ' ') for col in df9.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of business growth percent change by year for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

df12 = business_dynamics.reset_index()
fig = px.scatter(df12, x="year", y="percent_change", trendline="ols", hover_data=['estab_change','name'],
                labels={col:col.replace('_', ' ') for col in df12.columns}) # remove underscore)
fig.show()


# In[ ]:


#Plotly scatterplot of LOWESS regression trendline of business growth percent change by year for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

df12 = business_dynamics.reset_index()
fig = px.scatter(df12, x="year", y="percent_change", trendline="lowess", hover_data=['estab_change','name'],
                labels={col:col.replace('_', ' ') for col in df12.columns}) # remove underscore)
fig.show()


# ## One-Dimensional Distribution: Geographic Mobility

# Geographical Mobility based on US Census data from 2010-2019, including breakdowns by demographic characteristics and rates of inmigration, outmigration, and net migration. This is an important variable for comparing how geographic mobility has changed over time across the 27 cities and its potential correlation to the growth/declining factors of a thriving city.
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
# <b>from_abroad:</b> Moved from abroad. Estimate population 1 year and over.

# In[ ]:


#Read geographic mobility dataset, drop columns and create total mobility column
with open('data/geo_mobility.csv') as f:
    geo_mobility = pd.read_csv(f).drop(columns=['geo_id', 'city_state']) #.sort_values(by='year', ascending=False)
    geo_mobility['total_mobility_all'] = geo_mobility['same_county'] + geo_mobility['diff_county'] + geo_mobility['diff_state']+geo_mobility['from_abroad']
    geo_mobility['total_mobility_outside'] = geo_mobility['diff_county'] + geo_mobility['diff_state']+geo_mobility['from_abroad']
geo_mobility


# In[ ]:


geo_mobility['name'].drop_duplicates()#.count()


# In[ ]:


geo_mobility.shape


# In[ ]:


geo_mobility.value_counts()


# In[ ]:


#Seaborn Bar graph of total mobility for each city per year. Estimate population 1 year and over

geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'total_mobility_all').set(xlabel='Year', 
                                                ylabel='Total mobility per city. Estimate population 1 year and over')


# In[ ]:


#Seaborn Bar graph of total residential moves. Estimate population 1 year and over

geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'total_year').set(xlabel='Year', 
                                                ylabel='Total residential moves. Estimate population 1 year and over')


# In[ ]:


#Seaborn Bar graph of residential moves within the same county within each city per year. Estimate population 1 year and over
geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'same_county').set(xlabel='Year', 
                                        ylabel='Residential moves within the same county. Estimate population 1 year and over')


# In[ ]:


#Seaborn Bar graph of residential moves from a different county within each city per year. Estimate population 1 year and over
geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'diff_county').set(xlabel='Year', 
                                    ylabel='Residential moves from a different county. Estimate population 1 year and over')


# In[ ]:


#Seaborn Bar graph of residential moves from a different state per year. Estimate population 1 year and over
geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'diff_state').set(xlabel='Year', 
                                    ylabel='Residential moves from a different state. Estimate population 1 year and over')


# In[ ]:


#Seaborn Bar graph of residential moves from abroad per year. Estimate population 1 year and over
geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.barplot,x='year', y = 'from_abroad').set(xlabel='Year', 
                                            ylabel='Residential moves from abroad. Estimate population 1 year and over')


# In[ ]:


#Seaborn Line graph of total mobility for each city per year. Estimate population 1 year and over

geo_mob1 = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex
                                      =False, margin_titles=True)
geo_mob1.map_dataframe(sns.lineplot,x='year', y = 'total_mobility_all').set(xlabel='Year', 
                                                ylabel='Total mobility per city. Estimate population 1 year and over')


# In[ ]:


#Seaborn Line graph of total residential moves. Estimate population 1 year and over

geo_mob_line = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
geo_mob_line.map_dataframe(sns.lineplot,x='year',y='total_year').set(xlabel='Year', 
                                                ylabel='total residential moves. Estimate population YoY')


# In[ ]:


#Seaborn Line graph of residential moves within the same county. Estimate population 1 year and over

geo_mob_line = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
geo_mob_line.map_dataframe(sns.lineplot,x='year',y='same_county').set(xlabel='Year', 
                                            ylabel='residential moves within the same county. Estimate population YoY')


# In[ ]:


#Seaborn Line graph of residential moves from different county. Estimate population 1 year and over

geo_mob_line = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
geo_mob_line.map_dataframe(sns.lineplot,x='year',y='diff_county').set(xlabel='Year', 
                                                ylabel='residential moves from different county. Estimate population YoY')


# In[ ]:


#Seaborn Line graph of residential moves from different state. Estimate population 1 year and over

geo_mob_line = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
geo_mob_line.map_dataframe(sns.lineplot,x='year',y='diff_state').set(xlabel='Year', 
                                                ylabel='residential moves from different state. Estimate population YoY')


# In[ ]:


#Seaborn Line graph of residential moves from abroad. Estimate population 1 year and over

geo_mob_line = sns.FacetGrid(geo_mobility, col='name', col_wrap=3, height=5, aspect=1, sharex=False)
geo_mob_line.map_dataframe(sns.lineplot,x='year',y='from_abroad').set(xlabel='Year', 
                                                ylabel='residential moves from abroad. Estimate population YoY')


# In[ ]:


#Plotly Bar graph of Total Mobility (including same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df1 = geo_mobility.reset_index()

fig = px.bar(mob_df1, y='total_mobility_all', x="year", color='name', 
             title="Bar Plot of Total Mobility (including same county) by Year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in mob_df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Bar graph of Total Mobility (excluding same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df1 = geo_mobility.reset_index()

fig = px.bar(mob_df1, y='total_mobility_outside', x="year", color='name', 
             title="Bar Plot of Total Mobility (excluding same county) by Year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in mob_df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of Total Mobility (including same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df2 = geo_mobility.reset_index()
fig = px.line(mob_df2, x="year", y='total_mobility_all', color='name', 
              title="Line Plot of Total Mobility (including same county) by Year - 2010-2019",
              labels={col:col.replace('_', ' ') for col in mob_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of Total Mobility (excluding same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df2 = geo_mobility.reset_index()
fig = px.line(mob_df2, x="year", y='total_mobility_outside', color='name', 
              title="Line Plot of Total Mobility (excluding same county) by Year - 2010-2019",
              labels={col:col.replace('_', ' ') for col in mob_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotyly Scatterplot of Total Mobility (including same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df3 = geo_mobility.reset_index()
fig = px.scatter(mob_df3, x="year", y='total_mobility_all', 
                 color='name', symbol='name', #marginal_y="rug", 
                 title="Scatterplot of Total Mobility (including same county) by Year - 2010-2019",
                 labels={col:col.replace('_', ' ') for col in mob_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotyly Scatterplot of Total Mobility (excluding same county) by Year - 2010-2019. Estimate population 1 year and over

mob_df3 = geo_mobility.reset_index()
fig = px.scatter(mob_df3, x="year", y='total_mobility_outside', 
                 color='name', symbol='name', #marginal_y="rug", 
                 title="Scatterplot of Total Mobility (excluding same county) by Year - 2010-2019",
                 labels={col:col.replace('_', ' ') for col in mob_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Histogram of Total Mobility (including same county) by Year - 2010-2019. Estimate population 1 year and over
mob_df4 = geo_mobility.reset_index()
fig = px.histogram(mob_df4, x="year", y='total_mobility_all', color='name', 
                title="Histogram of Total Mobility by Year - 2010-2019", 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = mob_df4.columns,
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in mob_df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Histogram of Total Mobility (excluding same county) by Year - 2010-2019. Estimate population 1 year and over
mob_df4 = geo_mobility.reset_index()
fig = px.histogram(mob_df4, x="year", y='total_mobility_outside', color='name', 
                title="Histogram of Total Mobility by Year - 2010-2019", 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = mob_df4.columns,
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in mob_df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Histogram of total count of residential moves by Year - 2010-2019. Estimate population 1 year and over
mob_df4 = geo_mobility.reset_index()
fig = px.histogram(mob_df4, x="year", y='total_year', color='name', 
                title="Histogram of total count of residential moves by year - 2010-2019", 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = mob_df4.columns,
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in mob_df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Scatter Matrix of Total Mobility (including same county) by Year - 2010-2019. Estimate population 1 year and over
mob_df5 = geo_mobility.reset_index()
fig = px.scatter_matrix(mob_df5, dimensions=["year","total_mobility_all"],
    color="name", title="Scatter Matrix of Total Mobility by Year - 2010-2019",
    labels={col:col.replace('_', ' ') for col in mob_df5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatter Matrix of Total Mobility (excluding same county) by Year - 2010-2019. Estimate population 1 year and over
mob_df5 = geo_mobility.reset_index()
fig = px.scatter_matrix(mob_df5, dimensions=["year","total_mobility_outside"],
    color="name", title="Scatter Matrix of Total Mobility by Year - 2010-2019",
    labels={col:col.replace('_', ' ') for col in mob_df5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Total Mobility (including same county) by City - 2010-2019. Estimate population 1 year and over
mob_df6 = geo_mobility.reset_index()
fig = px.violin(mob_df6, y='total_mobility_all', x='year', box=True, color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Total Mobility (including same county) by City - 2010-2019", hover_data=mob_df6.columns,
                labels={col:col.replace('_', ' ') for col in mob_df6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Total Mobility (exluding same county) by City - 2010-2019. Estimate population 1 year and over
mob_df6 = geo_mobility.reset_index()
fig = px.violin(mob_df6, y='total_mobility_outside', x='year', box=True, color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Total Mobility (exluding same county) by City - 2010-2019", hover_data=mob_df6.columns,
                labels={col:col.replace('_', ' ') for col in mob_df6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Total Mobility (including same county) per year - 2010-2019. Estimate population 1 year and over
mob_df7 = geo_mobility.reset_index()
fig = px.violin(mob_df7, y="year", x='total_mobility_all', box=True, color='year',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Total Mobility (including same county) per Year - 2010-2019", hover_data=mob_df7.columns,
    labels={col:col.replace('_', ' ') for col in mob_df7.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Total Mobility (excluding same county) per year - 2010-2019. Estimate population 1 year and over
mob_df7 = geo_mobility.reset_index()
fig = px.violin(mob_df7, y="year", x='total_mobility_outside', box=True, color='year',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Total Mobility per Year - 2010-2019", hover_data=mob_df7.columns,
    labels={col:col.replace('_', ' ') for col in mob_df7.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Quantiles of Total Mobility (including same county) per year - 2010-2019. Estimate population 1 year and over
mob_df8 = geo_mobility.reset_index()
fig = px.violin(mob_df8, y="total_mobility_all", x='year', box=True, color='year',# draw box plot inside the violin
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Quantiles of Total Mobility (including same county) per year - 2010-2019", hover_data=['name'],
                labels={col:col.replace('_', ' ') for col in mob_df8.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of Quantiles of Total Mobility (excluding same county) per year - 2010-2019. Estimate population 1 year and over
mob_df8 = geo_mobility.reset_index()
fig = px.violin(mob_df8, y="total_mobility_outside", x='year', box=True, color='year',# draw box plot inside the violin
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of Quantiles of Total Mobility (excluding same county) per year - 2010-2019", hover_data=['name'],
                labels={col:col.replace('_', ' ') for col in mob_df8.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Box Plot of Total Mobility (including same county) by year with outliers - 2010-2019

mob_df9 = geo_mobility.reset_index()
fig = px.box(mob_df9, x='year', y='total_mobility_all', points='all', # can be 'all', 'outliers', or False
             title="Box Plot of Total Mobility (including same county) by year with outliers - 2010-2019", hover_data=mob_df9.columns,
             labels={col:col.replace('_', ' ') for col in mob_df9.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Box Plot of Total Mobility (excluding same county) by year with outliers - 2010-2019

mob_df9 = geo_mobility.reset_index()
fig = px.box(mob_df9, x='year', y='total_mobility_outside', points='all', # can be 'all', 'outliers', or False
             title="Box Plot of Total Mobility (excluding same county) by year with outliers - 2010-2019", hover_data=mob_df9.columns,
             labels={col:col.replace('_', ' ') for col in mob_df9.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

mob_df12 = geo_mobility.reset_index()
fig = px.scatter(mob_df12, x="year", y="total_mobility_all", trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (including same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in mob_df12.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (excluding same county) for each city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

mob_df12 = geo_mobility.reset_index()
fig = px.scatter(mob_df12, x="year", y="total_mobility_outside", trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (excluding same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in mob_df12.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of LOWESS regression trendline of total mobility by year (including same county) for each city.  
#Hovering over the trendline will show the equation of the line and its R-squared value.
#No visible changes in comparison to the OLS scatterplot

mob_df12 = geo_mobility.reset_index()
fig = px.scatter(mob_df12, x="year", y="total_mobility_all", trendline="lowess", 
                 title="Scatterplot of LOWESS trendline of Total Mobility (including same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in mob_df12.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of LOWESS regression trendline of total mobility by year (excluding same county) for each city.  
#Hovering over the trendline will show the equation of the line and its R-squared value.
#No visible changes in comparison to the OLS scatterplot

mob_df12 = geo_mobility.reset_index()
fig = px.scatter(mob_df12, x="year", y="total_mobility_outside", trendline="lowess", 
                 title="Scatterplot of LOWESS trendline of Total Mobility (excluding same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in mob_df12.columns}) # remove underscore
fig.show()


# In[ ]:


print(geo_mobility.corr().loc['year', 'total_mobility_all'])


# In[ ]:


print(geo_mobility.corr().loc['year', 'total_mobility_outside'])


# # CORRELATION: Business Dynamics Growth / Geographic Mobility

# In[ ]:


#Merge business_dynamics and geo_mobility datasets for visualization of possible correlations
bgrowth_geomob = pd.merge(business_dynamics, geo_mobility, on=['name','year'])
bgrowth_geomob


# In[ ]:


#pandas-profiling html analytics report for Business Dynamics & Geo Mobility dataset

pandas_profiling.ProfileReport(bgrowth_geomob) 


# In[ ]:


#DO NOT RERUN CELLS BELOW - already downloaded to html file in Sweetviz folder
#UNLESS a new report is needed.
#creating df for sweetviz analytics report focused on 'percent change' and 'total mobility'

#df = bgrowth_geomob
#my_report  = sweetviz.analyze([df,'percent_change'], target_feat='total_mobility')
#my_report.show_html('bgrowth_geomob_FinalReport.html')


# <b>The Pearson numerical association between total mobility and percent change is 0.11.</b>

# In[ ]:


bgrowth_geomob.dtypes


# In[ ]:


#dropping unnecessary columns
bgrowth_geomob_c = bgrowth_geomob.drop(columns=['firms', 'emp', 'estab',])
bgrowth_geomob_c 


# In[ ]:


#initial calculation and visualization of monotonic relationship between
#business dynamics/growth % and total mobility using Spearman correlation coefficient
bgrowth_geomob_c.corr('spearman').style.background_gradient(cmap="Blues")


# <b>The Spearman correlation score between percent change in active establishments YoY and total mobility of residents is 0.120670. <br>
# The association between the two variables is positive however weak.</b>

# In[ ]:


#initial calculation and visualization of possible linear relationship between
#business dynamics/growth % and total mobility using Pearson correlation coefficient to summarize its strength 
bgrowth_geomob_c.corr().style.background_gradient(cmap="Blues")


# <b>The linear correlation score between percent change in active establishments YoY and total mobility of residents is  0.105691.<br>
# The association between the two variables is positive however weak.</b>

# In[ ]:


#Pearson correlation coefficient score between 'percent_change', 'total_mobility_all' (including same county)

print(bgrowth_geomob_c.corr().loc['percent_change', 'total_mobility_all'])


# In[ ]:


#Pearson correlation coefficient score between 'percent_change', 'total_mobility_outside' (excluding same county)
print(bgrowth_geomob_c.corr().loc['percent_change', 'total_mobility_outside'])


# In[ ]:


#Seaborn Bar graph of total mobility for each city per year in comparison to percentage change of business growth per year.

bgrowth_geomob1 = sns.FacetGrid(bgrowth_geomob_c, col='name', col_wrap=2, height=5, aspect=2, sharex
                                      =False, margin_titles=True)
bgrowth_geomob1.map_dataframe(sns.barplot,x='total_mobility_all', y = 'percent_change').set(xlabel='Total mobility per city', 
                                                ylabel='Business Growth % YoY')


# In[ ]:


#Plotly Bar graph of total mobility (including same county) for each city per year in comparison to percentage change of business growth per year.

bgrowth_geomob2 = bgrowth_geomob_c.reset_index()

fig = px.bar(bgrowth_geomob2, x='total_mobility_all', y='percent_change', color='name', 
             title="Bar graph of total mobility (including same county) per year in comparison to % change of business growth per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in bgrowth_geomob2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Bar graph of total mobility (excluding same county) for each city per year in comparison to percentage change of business growth per year.

bgrowth_geomob2 = bgrowth_geomob_c.reset_index()

fig = px.bar(bgrowth_geomob2, x='total_mobility_outside', y='percent_change', color='name', 
             title="Bar graph of total mobility (excluding same county) per year in comparison to % change of business growth per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in bgrowth_geomob2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotyly Scatterplot of total mobility (including same county) for each city per year in comparison to percentage change of business growth per year.

bgrowth_geomob3 = bgrowth_geomob_c.reset_index()
fig = px.scatter(bgrowth_geomob3, x='total_mobility_all', y='percent_change', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility (including same county) per year in comparison to % change of business growth per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in bgrowth_geomob3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotyly Scatterplot of total mobility (excluding same county) for each city per year in comparison to percentage change of business growth per year.

bgrowth_geomob3 = bgrowth_geomob_c.reset_index()
fig = px.scatter(bgrowth_geomob3, x='total_mobility_outside', y='percent_change', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility (excluding same county) per year in comparison to % change of business growth per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in bgrowth_geomob3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Histogram of total mobility (including same county) for each city per year in comparison to percentage change of business growth per year.
bgrowth_geomob4 = bgrowth_geomob_c.reset_index()
fig = px.histogram(bgrowth_geomob4, x='total_mobility_all', y='percent_change', color='name', 
                title='Histogram of sum of total mobility (including same county)  per year in comparison to % change of business growth per year - 2010-2019', 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['percent_change', 'total_mobility_all'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Histogram of total mobility (excluding same county) for each city per year in comparison to percentage change of business growth per year.
bgrowth_geomob4 = bgrowth_geomob_c.reset_index()
fig = px.histogram(bgrowth_geomob4, x='total_mobility_outside', y='percent_change', color='name', 
                title='Histogram of sum of total mobility (excluding same county)  per year in comparison to % change of business growth per year - 2010-2019', 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['percent_change', 'total_mobility_outside'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Histogram of sum of total mobility (including same county) for each city per year in comparison to percentage change of business growth per year.
bgrowth_geomob4 = bgrowth_geomob_c.reset_index()
fig = px.histogram(bgrowth_geomob4, x='total_mobility_all', y='percent_change', color='name', 
                title='Histogram of sum of total mobility (including same county) per year in comparison to % change of business growth per year - 2010-2019', 
                barmode = 'group', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['percent_change', 'total_mobility_all'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Histogram of sum of total mobility (excluding same county) for each city per year in comparison to percentage change of business growth per year.
bgrowth_geomob4 = bgrowth_geomob_c.reset_index()
fig = px.histogram(bgrowth_geomob4, x='total_mobility_outside', y='percent_change', color='name', 
                title='Histogram of sum of total mobility (excluding same county) per year in comparison to % change of business growth per year - 2010-2019', 
                barmode = 'group', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['percent_change', 'total_mobility_outside'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Box plot of total mobility (including same county) for each city in comparison to % change of business growth per year.
bgrowth_geomob5 = bgrowth_geomob_c.reset_index()
fig = px.box(bgrowth_geomob5, x='total_mobility_all', y='percent_change', points='outliers', # can be 'all', 'outliers', or False
             title="Box Plot of total mobility (including same county) for each city in comparison to % change of business growth per year. - 2010-2019", hover_data=bgrowth_geomob5.columns,
             labels={col:col.replace('_', ' ') for col in bgrowth_geomob5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Box plot of total mobility (excluding same county) for each city per year in comparison to percentage change of business growth per year.
bgrowth_geomob5 = bgrowth_geomob_c.reset_index()
fig = px.box(bgrowth_geomob5, x='total_mobility_outside', y='percent_change', points='outliers', # can be 'all', 'outliers', or False
             title="Box Plot of total mobility (excluding same county) for each city in comparison to % change of business growth per year. - 2010-2019", hover_data=bgrowth_geomob5.columns,
             labels={col:col.replace('_', ' ') for col in bgrowth_geomob5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) 
#for each city in comparison to percentage change of business growth per year.. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

bgrowth_geomob6 = bgrowth_geomob_c.reset_index()
fig = px.scatter(bgrowth_geomob6, x='total_mobility_all', y='percent_change', trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (including same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (excluding same county) 
#for each city in comparison to percentage change of business growth per year.. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

bgrowth_geomob6 = bgrowth_geomob_c.reset_index()
fig = px.scatter(bgrowth_geomob6, x='total_mobility_outside', y='percent_change', trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (excluding same county) by year - 2010-2019",
                 hover_data=['total_year','name'],
                labels={col:col.replace('_', ' ') for col in bgrowth_geomob6.columns}) # remove underscore
fig.show()


# In[ ]:


bgrowth_geomob.dtypes


# In[ ]:


# Scatter with best fit line 
sns.regplot(x='percent_change', y='total_mobility_all',data=bgrowth_geomob, fit_reg=True)
plt.show()


# In[ ]:


print(bgrowth_geomob.corr().loc['percent_change', 'total_mobility_all'])


# In[ ]:


print(bgrowth_geomob.corr().loc['percent_change', 'total_mobility_outside'])


# In[ ]:


print(bgrowth_geomob.corr().loc['estab_change', 'total_mobility_all'])


# In[ ]:


print(bgrowth_geomob.corr().loc['estab_change', 'total_mobility_outside'])


# # One-Dimensional Distribution: Unemployment

# Annual employment data collected by the US Census, for 2010-2019. Includes breakdown by demographic categories and specifically unemployment rate, which is what I'll will be using for further analysis and modeling.
# 

# In[ ]:


#Read unemployment dataset, drop columns 
with open('data/unemployment.csv') as f:
    unemployment = pd.read_csv(f).drop(columns=['city_state']) #.sort_values(by='year', ascending=False)
    
unemployment


# In[ ]:


#creating a separate df specific for pandas-profiling html analytics report for 'unemployment'

df = pd.read_csv('data/unemployment.csv')
pandas_profiling.ProfileReport(df)


# In[ ]:


#Plotly Bar graph of unemployment rate by year - 2010-2019. Estimate population 1 year and over

unemp_df1 = unemployment.reset_index()

fig = px.bar(unemp_df1, y='unemployment_rate', x="year", color='name', 
             title="Bar Plot of unemployment rate by year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in unemp_df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Line plot of unemployment rate by year - 2010-2019. Estimate population 1 year and over

unemp_df2 = unemployment.reset_index()
fig = px.line(unemp_df2, x="year", y='unemployment_rate', color='name', 
              title='Line Plot of unemployment rate by year - 2010-2019',
              labels={col:col.replace('_', ' ') for col in unemp_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of unemployment rate by year - 2010-2019. Estimate population 1 year and over

unemp_df3 = unemployment.reset_index()
fig = px.scatter(unemp_df3, x="year", y='unemployment_rate', color='name',
                 symbol='name', #marginal_y="rug", 
                 title='Scatterplot of unemployment rate by year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in unemp_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of unemployment rate by city per year - 2010-2019. Estimate population 1 year and over

unemp_df3 = unemployment.reset_index()
fig = px.scatter(unemp_df3, x='name', y='unemployment_rate', color='year',
                 #symbol='year', #marginal_y="rug", 
                 title='Scatterplot of unemployment rate by city per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in unemp_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Histogram of unemployment rate by city per year - 2010-2019. Estimate population 1 year and over
unemp_df4 = unemployment.reset_index()
fig = px.histogram(unemp_df4, x='name', y='unemployment_rate', color='year', 
                title="Histogram of Total Mobility by Year - 2010-2019", 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = unemp_df4.columns,
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in unemp_df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Violin Plot of unemployment rate by city per year - 2010-2019. Estimate population 1 year and over
unemp_df6 = unemployment.reset_index()
fig = px.violin(unemp_df6, x='year', y='unemployment_rate', color='year',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of unemployment rate by city per year with outlier- 2010-2019", hover_data=unemp_df6.columns,
                labels={col:col.replace('_', ' ') for col in unemp_df6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of unemployment rate by city per year - 2010-2019. Estimate population 1 year and over
unemp_df7 = unemployment.reset_index()
fig = px.violin(unemp_df7, x='year', y='unemployment_rate', color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of unemployment rate by city per year - 2010-2019", hover_data=unemp_df7.columns,
                labels={col:col.replace('_', ' ') for col in unemp_df7.columns}) # remove underscore
fig.show()


# # CORRELATION: Business Dynamics Growth / Unemployment

# In[ ]:


#Merge business_dynamics and unemployment datasets for visualization of possible correlations
bgrowth_unemp = pd.merge(business_dynamics, unemployment, on=['name','year']) #.drop(columns=['firms','estab'])
bgrowth_unemp


# In[ ]:


bgrowth_unemp.dtypes


# In[ ]:


#creating pandas-profiling html analytics report for 'business dynamics' and unemployment'

pandas_profiling.ProfileReport(bgrowth_unemp)


# In[ ]:


#DO NOT RERUN CELLS BELOW - as report is already downloaded to html file in Sweetviz folder
#UNLESS a new report is needed.
#select a df column to analyze against target for sweetviz analytics report 

#df = bgrowth_unemp
#my_report  = sweetviz.analyze([df,'estab_change'], target_feat='unemployment_rate')
#my_report.show_html('bgrowth_estab_change_unemp_FinalReport.html')


# In[ ]:


#initial calculation and visualization of monotonic relationship between
#business dynamics/growth % and unemployment using Spearman correlation coefficient
bgrowth_unemp.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


#initial calculation and visualization of possible linear relationship between
#business dynamics/growth % and total mobility using Pearson correlation coefficient to summarize its strength 
bgrowth_unemp.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#Plotly Bar graph of unemployment for each city per year in comparison to percentage change of business growth per year.

bgrowth_unemp2 = bgrowth_unemp#.reset_index()

fig = px.bar(bgrowth_unemp2, x='unemployment_rate', y='percent_change', color='year', 
             title="Bar graph of unemployment rate per year in comparison to % change of business growth per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in bgrowth_unemp2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of unemployment for each city per year in comparison to percentage change of business growth per year.

bgrowth_unemp3 = bgrowth_unemp.reset_index()
fig = px.scatter(bgrowth_unemp3, x='unemployment_rate', y='percent_change', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of unemployment rate per year in comparison to % change of business growth per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in bgrowth_unemp3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Histogram of unemployment for each city per year in comparison to percentage change of business growth per year.

bgrowth_unemp4 = bgrowth_unemp.reset_index()
fig = px.histogram(bgrowth_unemp4, x='unemployment_rate', y='percent_change', color='name', 
                title='Histogram of unemployment rate per year in comparison to % change of business growth per year - 2010-2019', 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = ['percent_change', 'unemployment_rate'],
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in bgrowth_unemp4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly line graph of Unemployment Rate in correlation to Business Growth %
bgrowth_unemp5 = bgrowth_unemp.reset_index()
fig = px.line(bgrowth_unemp5, x="unemployment_rate", y='percent_change', color='name', 
              title="Line Plot of Unemployment Rate in correlation to Business Growth %  - 2010-2019",
              labels={col:col.replace('_', ' ') for col in bgrowth_unemp5.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotyly Scatter matrix of unemployment for each city per year in comparison to percentage change of business growth per year.
bgrowth_unemp6 = bgrowth_unemp.reset_index()
fig = px.scatter_matrix(bgrowth_unemp6, dimensions=["percent_change", "unemployment_rate"],
    color="year", title="Scatter Matrix of Business Growth Percent Change and Unemployment Rate by Year",
    labels={col:col.replace('_', ' ') for col in bgrowth_unemp6.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly violin plot of unemployment for each city per year in comparison to percentage change of business growth per year.

bgrowth_unemp7 = bgrowth_unemp.reset_index()
fig = px.violin(bgrowth_unemp7, y="unemployment_rate", x='percent_change', box=True, color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of unemployment rate for each city per year vs. % change in business growth by City - 2010-2019",
                hover_data=bgrowth_unemp7.columns,
                labels={col:col.replace('_', ' ') for col in bgrowth_unemp7.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Violin Plot of unemployment rate for each city per year in comparison to percentage change of business growth per year.
bgrowth_unemp8 = bgrowth_unemp.reset_index()
fig = px.violin(bgrowth_unemp8, x='percent_change', y='unemployment_rate', box=True, color='year',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of unemployment rate for each city per year vs. % change in business growth by Year", hover_data=bgrowth_unemp8.columns,
                labels={col:col.replace('_', ' ') for col in bgrowth_unemp8.columns}) # remove underscore
fig.show()


# In[ ]:


bgrowth_unemp9 = bgrowth_unemp.reset_index()
fig = px.box(bgrowth_unemp9, x='unemployment_rate', y='percent_change', points='outliers', # can be 'all', 'outliers', or False
             title="Box Plot of Business Growth % Change vs. Unemployment Rate with outliers - 2010-2019", hover_data=bgrowth_unemp9.columns,
             labels={col:col.replace('_', ' ') for col in bgrowth_unemp9.columns}) # remove underscore
fig.show()


# In[ ]:


print(bgrowth_unemp.corr().loc['percent_change', 'unemployment_rate'])


# In[ ]:


print(bgrowth_unemp.corr().loc['estab_change', 'unemployment_rate'])


# # One-Dimensional Distribution: School Enrollment

# Data containing the enrollment numbers of students broken down by two indicators public vs. private school. Even more so enrollment numbers can also be previewed by age group (Age 3 and up, 10 to 14 years), type of school (Kindergarten, Undergraduate) and Grades (Elementary: grade 1 to grade 4 ,etc..). Primarily looking at enrollment numbers for Kindergarten to 12th grade over time to tell us how large the education system is in a city. Additionally enrollment #s in private vs public schools over the years indicates the quality of education in that city.
# 

# In[ ]:


#Read school enrollment dataset, drop columns 
with open('data/school_enrollment.csv') as f:
    enrolled = pd.read_csv(f).drop(columns=['city_state']) #.sort_values(by='year', ascending=False)
    enrolled['total_per_pub_pri'] = enrolled['percent_enrolled _Kto12public'] + enrolled['percent_enrolled _Kto12private']
enrolled


# In[ ]:


enrolled.dtypes


# In[ ]:


#creating pandas-profiling html analytics report for student enrollment in 2010-2019

pandas_profiling.ProfileReport(enrolled)


# In[ ]:


#DO NOT RERUN CELLS BELOW - already downloaded to html file in Sweetviz folder
#UNLESS a new report is needed.
#select a df column to analyze against target for sweetviz analytics report 

#df = enrolled
#my_report  = sweetviz.analyze([df,'name'], target_feat='percent_enrolled _Kto12public')
#my_report.show_html('percent_enrolled _Kto12public_by_city_FinalReport.html')


# In[ ]:


#DO NOT RERUN CELLS BELOW - already downloaded to html file in Sweetviz folder
#UNLESS a new report is needed.
#select a df column to analyze against target for sweetviz analytics report 

#df = enrolled
#my_report  = sweetviz.analyze([df,'name'], target_feat='total_enrolled_Kto12')
#my_report.show_html('school_enrollment_city_total_FinalReport.html')


# In[ ]:


#Plotly Bar graph of student enrollment % for public schools by year and city - 2010-2019. 

enrolled_df1 = enrolled.reset_index()

fig = px.bar(enrolled_df1, x='percent_enrolled _Kto12public', y='name',  color='year', 
             title="Bar Plot of public K-12 school enrollment by year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in enrolled_df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly line graph of student enrollment % for public schools by year and city - 2010-2019. 

enrolled_df2 = enrolled.reset_index()
fig = px.line(enrolled_df2, x='year', y='percent_enrolled _Kto12public', color='name', 
              title='Line Plot of public K-12 school enrollment by year - 2010-2019',
              labels={col:col.replace('_', ' ') for col in enrolled_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly line plot of student enrollment % for public schools by year and city - 2010-2019

enrolled_df2 = enrolled.reset_index()
fig = px.line(enrolled_df2, x='name', y='percent_enrolled _Kto12public', color='year',
                title="Line Plot of student enrollment % for public schools by year and city - 2010-2019", 
                hover_data=enrolled_df2.columns,
                labels={col:col.replace('_', ' ') for col in enrolled_df2.columns}) # remove underscore
fig.show()


# <b>In the bar plot below is visualized the total percentage of student enrollment by city and year identifying which cities have a higher number of students. </b>

# In[ ]:


#Plotly Bar graph of total student enrollment % for private schools by year and city - 2010-2019. 

enrolled_df1 = enrolled.reset_index()

fig = px.bar(enrolled_df1, x='total_enrolled_Kto12', y='name',  color='year', 
             title="Bar Plot of total enrolled K-12 by city and year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in enrolled_df1.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly line graph of student enrollment % for private schools by year and city - 2010-2019. 

enrolled_df2 = enrolled.reset_index()
fig = px.line(enrolled_df2, x='year', y='percent_enrolled _Kto12private', color='name', 
              title='Line Plot of private K-12 school enrollment by year - 2010-2019',
              labels={col:col.replace('_', ' ') for col in enrolled_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly line plot of student enrollment % for private schools by year and city - 2010-2019

enrolled_df2 = enrolled.reset_index()
fig = px.line(enrolled_df2, x='name', y='percent_enrolled _Kto12private', color='year',
                title="Line Plot of student enrollment % for private schools by year and city - 2010-2019", 
                hover_data=enrolled_df2.columns,
                labels={col:col.replace('_', ' ') for col in enrolled_df2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of student enrollment % for public schools by year and city - 2010-2019. 

enrolled_df3 = enrolled.reset_index()
fig = px.scatter(enrolled_df3, x="year", y='percent_enrolled _Kto12public', color='name',
                 symbol='name', #marginal_y="rug", 
                 title='Scatterplot of tudent enrollment % for public schools by year and city - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in enrolled_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of student enrollment % for private schools by year and city - 2010-2019. 

enrolled_df3 = enrolled.reset_index()
fig = px.scatter(enrolled_df3, x="year", y='percent_enrolled _Kto12private', color='name',
                 symbol='name', #marginal_y="rug", 
                 title='Scatterplot of student enrollment % for private schools by year and city - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in enrolled_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total student enrollment % for public and private schools by year and city - 2010-2019. 

enrolled_df3 = enrolled.reset_index()
fig = px.scatter(enrolled_df3, x="year", y='total_per_pub_pri', color='name',
                 symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total student enrollment % for public and private schools by year and city - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in enrolled_df3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Histogram of student enrollment % for public schools by year and city - 2010-2019

enrolled_df4 = enrolled.reset_index()
fig = px.histogram(enrolled_df4, x='name', y='percent_enrolled _Kto12public', color='year', 
                title="Histogram of public K-12 school enrollment by year - 2010-2019", 
                barmode = 'stack', #barmode options for px.histograms: 'stack', 'group', or 'overlay'
                barnorm = None, #barnorm options for px.histogram: None, 'fraction', or 'percent'
                hover_data = enrolled_df4.columns,
                #animation_frame="name",
                #range_x=[0,df4["percent_change"].max()*1.1],
                #histfunc = 'count', #histfunc options for px.histograms: 'count', 'sum', 'avg', 'max', or 'min'
                facet_col = 'name', facet_col_wrap=3, facet_row_spacing=0.08,
                labels={col:col.replace('_', ' ') for col in enrolled_df4.columns}) # remove underscore

#fig.update_xaxes(type='category')
                   
fig.show()


# In[ ]:


#Plotly Violin Plot of student enrollment % for public schools by year and city - 2010-2019

enrolled_df5 = enrolled.reset_index()
fig = px.violin(enrolled_df5, x='year', y='percent_enrolled _Kto12public', color='name',
                points='all', # can be 'all', 'outliers', or False
                title="Violin Plot of student enrollment % for public schools by year and city - 2010-2019", 
                hover_data=enrolled_df5.columns,
                labels={col:col.replace('_', ' ') for col in enrolled_df5.columns}) # remove underscore
fig.show()


# In[ ]:


enrolled.dtypes


# # CORRELATION: Geographic Mobility / School Enrollment

# To better understand the possible correlation between geographic mobility and school enrollment from K-12 per city and by year, we visualized the data using Plotly. The variables we are primarily interested in for the initial hypothesis are the total number of students enrolled and the total geographic mobility by city per year. I also looked at whether there is a difference in calculating geographic mobility within the same county and geographic mobility from different counties, states and from abroad. 

# In[ ]:


#Merging geo_mobility and school enrollment datasets for visualization of possible correlations
geomob_enroll = pd.merge(geo_mobility, enrolled, on=['name','year']) #.drop(columns=['firms','estab'])
geomob_enroll


# In[ ]:


#creating pandas-profiling html analytics report for 'geo mobility' and 'school enrollment'

pandas_profiling.ProfileReport(geomob_enroll)


# In[ ]:


#DO NOT RERUN CELLS BELOW - already downloaded to html file in Sweetviz folder
#UNLESS a new report is needed.
#select a df column to analyze against target for sweetviz analytics report 

#df = geomob_enroll
#my_report  = sweetviz.analyze([df,'total_enrolled_Kto12'], target_feat='percent_enrolled_Kto12private')
#my_report.show_html('percent_enrolled _Kto12private_FinalReport.html')


# In[ ]:


#initial calculation and visualization of monotonic relationship between geo mobility and school enrollment
#using Spearman correlation coefficient
geomob_enroll.corr('spearman').style.background_gradient(cmap="Blues")


# In[ ]:


#initial calculation and visualization of possible linear relationship between
#geo mobility and school enrollment using Pearson correlation coefficient to summarize its strength 
geomob_enroll.corr().style.background_gradient(cmap="Blues")


# In[ ]:


#Plotly Bar graph of total mobility (including same county) for each city per year in comparison to total number of school enrollment per year.

geomob_enroll2 = geomob_enroll.reset_index()

fig = px.bar(geomob_enroll2, x='total_mobility_all', y='total_enrolled_Kto12', color='name', 
             title="Bar graph of total mobility (including same county) per year in comparison to total school enrollment K-12 per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in geomob_enroll2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Bar graph of total mobility (excluding same county) for each city per year in comparison to total school enrollment per year.

geomob_enroll2 = geomob_enroll.reset_index()

fig = px.bar(geomob_enroll2, x='total_mobility_outside', y='total_enrolled_Kto12', color='name', 
             title="Bar graph of total mobility (excluding same county) per year in comparison to total school enrollment per year - 2010-2019",
             labels={col:col.replace('_', ' ') for col in geomob_enroll2.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total mobility (including same county) for each city per year in comparison to total enrollment per year.

geomob_enroll3 = geomob_enroll
#geomob_enroll3_grouped = geomob_enroll3.groupby(['name','year'], as_index=False).mean()
fig = px.scatter(geomob_enroll3, x='total_mobility_all', y='total_enrolled_Kto12', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility (including same county) per year' 
                         ' in comparison to total school enrollment per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
#fig.add_scatter(y=geomob_enroll3.total_mobility_all)
fig.show()


# In[ ]:


#Plotly Line plot of total mobility (including same county) for each city per year in comparison to total enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.line(geomob_enroll3, x='total_mobility_all', y='total_enrolled_Kto12', color='name', 
                 title='Line plot of total mobility (including same county) per year' 
                         ' in comparison to total school enrollment per year - 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore

fig.show()


# In[ ]:


#Plotly Scatterplot of total mobility (including same county) for each city per year in comparison to percentage of school enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll3, x='total_mobility_all', y='total_enrolled_Kto12', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility (including same county) in comparison to % of enrolled K-12 public per year and city, 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total mobility (excluding same county) for each city per year in comparison to % of K-12 school enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll3, x='total_mobility_outside', y='percent_enrolled _Kto12public', color='name', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility (excluding same county) in comparison to % of enrolled K-12 public per year and city, 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total number of geo mobilities recorded for each city per year in comparison to percentage of K-12 public school enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll3, x='total_year', y='percent_enrolled _Kto12public', color='year', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility in comparison to % of enrolled K-12 public per year and city, 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total mobility (including same county) for each city per year in comparison to percentage of K-12 public school enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll3, x='total_mobility_all', y='total_enrolled_Kto12', color='year', symbol='name', #marginal_y="rug", 
                 title='Scatterplot of total mobility in comparison to % of enrolled K-12 public per year and city, 2010-2019',
                 labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly Scatterplot of total mobility (including same county) for each city per year in comparison to percentage of K-12 public school enrollment per year.

geomob_enroll3 = geomob_enroll.reset_index()
fig = px.box(geomob_enroll3, x='total_mobility_all', y='total_enrolled_Kto12', points='outliers', # can be 'all', 'outliers', or False
             title="Box Plot of total mobility (including same county) in comparision to % of enrolled K-12 public per year and city, 2010-2019", 
             hover_data=geomob_enroll3.columns,
             labels={col:col.replace('_', ' ') for col in geomob_enroll3.columns}) # remove underscore
fig.show()


# In[ ]:


geomob_enroll.dtypes


# <b>Below is scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) for each city in comparison to the total number of enrolled students from K-12 per city. Hovering over the trendline will show the equation of the line and its R-squared value. When looking at the data in this manner, I am able to visualize that the geographic mobility does not directly correlate to the total number of students enrolled. </b>
# 

# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (including same county) 
#for each city in comparison to the total number of students enrolled in K-12 per city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

geomob_enroll4 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll4, x='total_mobility_all', y='total_enrolled_Kto12', trendline="ols", 
                 title="Scatterplot of OLS trendline of total mobility (ALL) & total enrolled K-12 - 2010-2019",
                 hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in geomob_enroll4.columns}) # remove underscore
fig.show()


# In[ ]:


#Plotly scatterplot of Ordinary Least Squares regression trendline of total mobility by year (excluding same county) 
#for each city in comparison to the total number of students enrolled in K-12 per city. 
#Hovering over the trendline will show the equation of the line and its R-squared value.

geomob_enroll4 = geomob_enroll.reset_index()
fig = px.scatter(geomob_enroll4, x='total_mobility_outside', y='total_enrolled_Kto12', trendline="ols", 
                 title="Scatterplot of OLS trendline of Total Mobility (excluding same county) by year - 2010-2019",
                 hover_data=['year','name'],
                labels={col:col.replace('_', ' ') for col in geomob_enroll4.columns}) # remove underscore
fig.show()


# In[ ]:


geomob_enroll.dtypes


# In[ ]:


print(geomob_enroll.corr().loc['total_mobility_all', 'total_per_pub_pri'])


# In[ ]:


print(geomob_enroll.corr().loc['total_mobility_all', 'total_enrolled_Kto12'])


# In[ ]:


print(geomob_enroll.corr().loc['total_mobility_outside', 'total_enrolled_Kto12'])


# Furthermore, Person’s correlation coefficient score for 'total_mobility_all', 'total_enrolled_Kto12' is -0.202 verifying that there is negative correlation between the two variables.

# Please refer to notebook 2 for continued analysis.</b>

# Author - Veronica Huxley 
