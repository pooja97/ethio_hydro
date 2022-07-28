#standard imports
import pandas as pd
import numpy as np
import streamlit as st
import os
import glob


#imports for finding the nearest lat long using haversine distance
from math import radians, cos, sin, asin, sqrt
import math

#visualization libraries to visualize different plots
import plotly.express as px
import plotly.graph_objects as go
import altair as alt


#for Logo plotting
from PIL import Image

#for Folium Map Creation
from typing import Dict, List, Optional
import folium
from streamlit_folium import st_folium
from branca.element import Figure
from precipitation_function import lat_long_type

#disabling warnings
import warnings
warnings.filterwarnings("ignore")

#For parallel processing
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)



fig = Figure(width = 550,height = 350)

#function for calculating annual average
@st.cache
def annual_avg(df,year_lst):
    annual_avg_df_lst = list()
    for i in year_lst:
        d = df.get_group((i))
        d['Annual avg'] = (d['daily_avg'].sum())/len(d)
        annual_avg_df_lst.append(d)
    return annual_avg_df_lst


#function for splitting the date column values into year, month and day
def df_date_split(df,lat_long_list):
    df_date_list = list()
    for i in lat_long_list:
        grouped_df = df.get_group(i)
        grouped_df[['Year','Month','Day']] = grouped_df['date'].str.split('-',expand = True)
        df_date_list.append(grouped_df)
    date_split_df = pd.concat(df_date_list)
    return date_split_df


@st.cache
#function for creating 2 separate columns one for country code with 'et' values and 2nd with lat long concated values
def lat_long_process(df):
    df['lat_long'] = df.loc[:,'lat'].astype(str)+','+df.loc[:,'long'].astype(str)
    df.drop_duplicates(inplace = True)
    return df

@st.cache
#Creating a separate dataframe for lat long values and returning a list of lat_long values
def lat_long_list_creation(df):
    lat_long_df = df[['lat','long']]
    lat_long_df['lat_long'] = lat_long_df.loc[:,'lat'].astype(str)+','+lat_long_df.loc[:,'long'].astype(str)
    lat_long_df.drop_duplicates(inplace=True)
    lat_long_list = lat_long_df['lat_long']
    return lat_long_list


#function for grouping the data on lat long and returning only the et lat long
def group_df(df,lat_long_lst):
    in_names = df.groupby(df['lat_long'])
    temperaturedf_new = list()
    for i in lat_long_lst:
        df1 = in_names.get_group(i)
        temperaturedf_new.append(df1)
    result = pd.concat(temperaturedf_new)
    return result


#function for calculating daily average
def daily_avg(x,y):
    return (x+y)/2



@st.cache
#creating avg dataframe
def annual_avg_plot(annual_avg_df,lat_long_option,lat_long_list):
    annual_avg_df = annual_avg_df.groupby('lat_long')
    annual_avg_df = df_date_split(annual_avg_df,lat_long_list)
    annual_avg_df = annual_avg_df.groupby('lat_long')
    annual_avg_df = annual_avg_df.get_group(lat_long_option)
    #returns the list of unique year values
    year_lst = annual_avg_df['Year'].unique()
    annual_avg_dataframe = annual_avg_df.groupby('Year')
    annual_avg_result = annual_avg(annual_avg_dataframe,year_lst)
    annual_average = pd.concat(annual_avg_result,axis = 0)
    return annual_average


#creating average temp plotly chart
def avg_temp_plot(annual_temp,lat_long_val):
    #CODE FOR PLOTTING ANNUAL AVERAGE TEMPERATURE
    fig_avg = px.line(annual_temp, x= 'Year',y='Annual avg')
    fig_avg.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_avg.update_traces(line_color ='dimgray')
    fig_avg.update_xaxes(gridcolor='whitesmoke')
    fig_avg.update_yaxes(gridcolor = 'whitesmoke')
    fig_avg.update_yaxes(title = 'Annual Average Temperature (C)')
    # fig_avg.update_layout(title = "Annual Average Temperature: "+str(lat_long_val))

    return fig_avg


@st.cache
def annual_min_plot(Annual_temp_min,option_annual_min_temp,lat_long_list):
    Annual_temp_min = Annual_temp_min.groupby('lat_long')
    Annual_temp_min = df_date_split(Annual_temp_min,lat_long_list)
    Annual_temp_min = Annual_temp_min.groupby(['lat_long','Year'])[['tmin']].min()
    Annual_temp_min.rename(columns = {'tmin':'Yearly_minimum_temp'},inplace = True)
    Annual_temp_min.reset_index(inplace = True)
    Annual_temp_min = Annual_temp_min.groupby('lat_long')
    df2 = Annual_temp_min.get_group(option_annual_min_temp)
    return df2

@st.cache
def annual_max_plot(Annual_temp,option_annual_temp,lat_long_list):
    Annual_temp = Annual_temp.groupby('lat_long')
    Annual_temp = df_date_split(Annual_temp,lat_long_list)
    Annual_temp = Annual_temp.groupby(['lat_long','Year'])[['tmax']].max()
    Annual_temp.rename(columns = {'tmax':'Yearly_maximum_temp'},inplace = True)
    Annual_temp.reset_index(inplace = True)
    Annual_temp = Annual_temp.groupby('lat_long')
    df1 = Annual_temp.get_group(option_annual_temp)
    return df1


@st.cache
def daily_avg_calc(result,option,start,end):
    grouped_temperature_df = result.groupby('lat_long')
    data_frame = grouped_temperature_df.get_group(option)
    data_frame.set_index('date',inplace = True)
    data_frame_start_end = data_frame.loc[str(start):str(end)]
    data_frame_start_end = data_frame_start_end.reset_index()
    return data_frame_start_end

def daily_avg_plot(data_frame_start_end,lat_long_val):
    #Plotting the line chart of the daily average
    fig  = px.line(data_frame_start_end, x = 'date',y='daily_avg',title = 'Daily Average Temperature')
    fig.update_traces(line_color = 'blue')
    fig.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig.update_yaxes(ticklabelposition="inside top", title= 'Daily Average Temperature (C)',gridcolor = 'whitesmoke')
    fig.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    # fig.update_layout(title = "Daily Average Temperature: "+str(lat_long_val))
    return fig

@st.cache
def monthly_mean_calc(temperature_monthly_df,lat_long_list):
    #monthly mean calculation
    temperature_monthly_df = temperature_monthly_df.groupby('lat_long')
    date_split_df = df_date_split(temperature_monthly_df,lat_long_list)
    monthly_avg_temp = date_split_df.groupby(['lat_long','Year','Month'])[['daily_avg']].mean()
    monthly_avg_temp.rename(columns = {'daily_avg':'Monthly mean temperature'},inplace = True)
    return monthly_avg_temp


@st.cache(ttl=24*60*60)
def selecting_mean(monthly_avg_temp,option_mean,start_year,end_year):
    monthly_avg_temp = monthly_avg_temp.reset_index().set_index('Year').groupby('lat_long')
    grouped_monthly_mean = monthly_avg_temp.get_group(option_mean)
    df = grouped_monthly_mean.loc[start_year:end_year]
    df = df.reset_index()
    return df


def plot_mean_data(df,lat_long_val):
    title_text = "Monthly Mean Temperature: "+str(lat_long_val)
    highlight = alt.selection(
    type='single', on='mouseover', fields=['Year'], nearest=True)
    base = alt.Chart(df,title = title_text).encode(
    x = alt.X('Month:Q',scale = alt.Scale(domain=[1,12]),axis=alt.Axis(tickMinStep=1)),
    y = alt.Y('Monthly mean temperature:Q',scale = alt.Scale(domain =[int(df['Monthly mean temperature'].min()),int(df['Monthly mean temperature'].max())])),
    color = alt.Color('Year:O',scale = alt.Scale(scheme = 'magma'))
    )
    points = base.mark_circle().encode(
    opacity=alt.value(0),
    tooltip=[
        alt.Tooltip('Year:O', title='Year'),
        alt.Tooltip('Month:Q', title='Month'),
        alt.Tooltip('Monthly mean temperature:Q', title='Mean temp')
    ]).add_selection(highlight)

    lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)))

    mean_chart = (points + lines).properties(width=1000, height=450).interactive()
    return mean_chart

def max_temp_plot(df_max,lat_long_val):
    fig_max = px.line(df_max,x = 'Year',y='Yearly_maximum_temp')
    fig_max.update_traces(line_color = 'maroon')
    fig_max.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_max.update_xaxes(gridcolor='whitesmoke')
    fig_max.update_yaxes(gridcolor = 'whitesmoke')
    fig_max.update_yaxes(title = "Annual Maximum Temperature (C)")
    # fig_max.update_layout(title = "Yearly Maximum Temperature: "+str(lat_long_val))

    return fig_max


def min_temp_plot(df_min,lat_long_val):
    fig_min = px.line(df_min, x= 'Year',y = 'Yearly_minimum_temp')
    fig_min.update_traces(line_color ='blue')
    fig_min.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_min.update_xaxes(gridcolor='whitesmoke')
    fig_min.update_yaxes(gridcolor = 'whitesmoke')
    fig_min.update_yaxes(title = "Annual Minimum Temperature (C)")
    # fig_min.update_layout(title = "Yearly Minimum Temperature: "+str(lat_long_val))

    return fig_min


#code for downloading Data as a CSV File
@st.cache
def convert_df(df):
     return df.to_csv().encode('utf-8')

# a = st.sidebar.empty()

#result dataframe contains the daily average value as well.
#Function for creating folium map and returning the latitude and Longitude of the clicked location
def map_creation(lat,long,clicked_lat,clicked_long):
    with st.sidebar:
        m = folium.Map(location = [9.14,40],zoom_start =7)
        fig.add_child(m)
        tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True).add_to(m)
        folium.TileLayer('Stamen Terrain').add_to(m)
        folium.TileLayer('Stamen Water Color').add_to(m)
        folium.LayerControl().add_to(m)
        if (clicked_lat == 0) and (clicked_long == 0):
            folium.Marker([lat,long]).add_to(m)
        else:
            folium.Marker([lat,long]).add_to(m)
            folium.Marker([clicked_lat,clicked_long]).add_to(m)
        st_data = st_folium(m,key = 'map_fig_1')
        return st_data

#df is the initial df that contains only et data
def search_func(latitude,longitude,lt_lng_lst,df):
    df['lat_radian'],df['long_radian'] = np.radians(df['lat']),np.radians(df['long'])
    df['dLON'] = df['long_radian'] - math.radians(longitude)
    df['dLAT'] = df['lat_radian'] - math.radians(latitude)
    df['distance'] = 6371 * 2 * np.arcsin(np.sqrt(np.sin(df['dLAT']/2)**2 + math.cos(math.radians(longitude)) * np.cos(df['lat_radian']) * np.sin(df['dLON']/2)**2))
    a = df['distance'].idxmin()
    nearest_neighbor = df._get_value(a,'lat_long')
    nearest_neighbor = lat_long_type(nearest_neighbor)
        # st.write("**Nearest Latitude and Longitude is :**",nearest_neighbor)
    return nearest_neighbor
