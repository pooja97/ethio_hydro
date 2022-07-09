#pip3 install geopy
#pip3 install -U pandarallel
#pip3 install geopy
#pip3 install glob
#pip3 install pydeck
#pip3 install pydeck-earthengine-layers
#pip3 install streamlit
#pip3 install streamlit-folium
#pip3 install folium
#pip3 install plotly


#standard imports
import pandas as pd
import numpy as np
import streamlit as st




#for reading multiple files together
import glob
import os


#for filtering the data not related to Ethopia
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

#imports for finding the nearest lat long using haversine distance
from math import radians, cos, sin, asin, sqrt
import math

#visualization libraries to visualize different plots
import seaborn as sns
import matplotlib.pyplot as plt
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

#disabling warnings
import warnings
warnings.filterwarnings("ignore")

#For parallel processing
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)


# Setting the Page Layout as wide
st.set_page_config(
    page_title="AI GERD Dashboard",
    layout="wide")

padding_top = 0


# Creating Container for Logo and Title
with st.container():
    col1,col2 = st.columns(2)
    #Code for adding Logo
    with col1:
        image = Image.open('require/image.png')
        st.image(image)
    #Code for Title
    with col2:
        col2.markdown("<h1 style='text-align:centre; color: black;'>ETHIO HYDRO</h1>", unsafe_allow_html=True)

#nearest neighbor
nn = 0

#setting the plot figure size
fig = Figure(width = 550,height = 350)

#reading CSV Files
temperatureFiles = os.path.join("require/historicalData/temperature*.csv")
temperatureFiles = glob.glob(temperatureFiles)
temperatureDF = pd.concat(map(pd.read_csv,temperatureFiles),ignore_index = True)

#data inspection
temperatureDF.info()

#creating copy of our dataframe
temperatureDataFrame = temperatureDF.copy()



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


#creating geolocator object for getting country code
geolocator = Nominatim(user_agent="geoapiExercises")

#function for fetching country code using geolocator
@st.cache
def locationFilter(lat_long):
    location = geolocator.reverse(lat_long,timeout=None,language='en')
    address = location.raw['address']
    return address['country_code']

@st.cache
#function for creating 2 separate columns one for country code with 'et' values and 2nd with lat long concated values
def lat_long_process(df):
    df['Country_code'] = 'et'
    df['lat_long'] = df.loc[:,'lat'].astype(str)+','+df.loc[:,'long'].astype(str)
    df.drop_duplicates(inplace = True)
    return df

#applying the function on the dataframe
temperatureDataFrame = lat_long_process(temperatureDataFrame)


#Creating a separate dataframe for lat long values and returning a list of lat_long values
@st.experimental_memo
def lat_long_list_creation(df):
    lat_long_df = df[['lat','long']]
    lat_long_df['lat_long'] = lat_long_df.loc[:,'lat'].astype(str)+','+lat_long_df.loc[:,'long'].astype(str)
    lat_long_df.drop_duplicates(inplace=True)
    lat_long_df['Country_code'] = lat_long_df['lat_long'].parallel_apply(lambda x:locationFilter(x))
    lat_long_df['Country_code'].unique()
    lat_long_df = lat_long_df[lat_long_df['Country_code']=='et']
    lat_long_list = lat_long_df['lat_long']
    return lat_long_list

#applying the lat long creation function on the dataframe
lat_long_list = lat_long_list_creation(temperatureDataFrame)

#function for grouping the data on lat long and returning only the et lat long
def group_df(df,lat_long_lst):
    in_names = df.groupby(df['lat_long'])
    temperaturedf_new = list()
    for i in lat_long_lst:
        df1 = in_names.get_group(i)
        temperaturedf_new.append(df1)
    result = pd.concat(temperaturedf_new)
    return result

#applying the function on the dataframe
result = group_df(temperatureDataFrame,lat_long_list)

#function for calculating daily average
def daily_avg(x,y):
    return (x+y)/2

#Dataframe containing daily average
result['daily_avg'] = result.parallel_apply(lambda x: daily_avg(x.tmin,x.tmax),axis=1)

@st.cache
#creating avg dataframe
def annual_avg_plot(annual_avg_df,lat_long_option):
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
    fig_avg = px.line(annual_temp, x= 'Year',y='Annual avg',title = 'Yearly Average Temperature')
    fig_avg.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_avg.update_traces(line_color ='dimgray')
    fig_avg.update_xaxes(gridcolor='whitesmoke')
    fig_avg.update_yaxes(gridcolor = 'whitesmoke')
    fig_avg.update_layout(title = "Yearly Average Temperature: "+str(lat_long_val))

    return fig_avg


@st.cache
def annual_min_plot(Annual_temp_min,option_annual_min_temp):
    Annual_temp_min = Annual_temp_min.groupby('lat_long')
    Annual_temp_min = df_date_split(Annual_temp_min,lat_long_list)
    Annual_temp_min = Annual_temp_min.groupby(['lat_long','Year'])[['tmin']].min()
    Annual_temp_min.rename(columns = {'tmin':'Yearly_minimum_temp'},inplace = True)
    Annual_temp_min.reset_index(inplace = True)
    Annual_temp_min = Annual_temp_min.groupby('lat_long')
    df2 = Annual_temp_min.get_group(option_annual_min_temp)
    return df2

@st.cache
def annual_max_plot(Annual_temp,option_annual_temp):
    Annual_temp = Annual_temp.groupby('lat_long')
    Annual_temp = df_date_split(Annual_temp,lat_long_list)
    Annual_temp = Annual_temp.groupby(['lat_long','Year'])[['tmax']].max()
    Annual_temp.rename(columns = {'tmax':'Yearly_maximum_temp'},inplace = True)
    Annual_temp.reset_index(inplace = True)
    Annual_temp = Annual_temp.groupby('lat_long')
    df1 = Annual_temp.get_group(option_annual_temp)
    return df1



@st.cache
def daily_avg_calc(result,option):
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
    fig.update_yaxes(ticklabelposition="inside top", title= 'Daily average temperature',gridcolor = 'whitesmoke')
    fig.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_layout(title = "Daily Average Temperature: "+str(lat_long_val))
    return fig

@st.cache
def monthly_mean_calc(temperature_monthly_df,lat_long_list):
    #monthly mean calculation
    temperature_monthly_df = temperature_monthly_df.groupby('lat_long')
    date_split_df = df_date_split(temperature_monthly_df,lat_long_list)
    monthly_avg_temp = date_split_df.groupby(['lat_long','Year','Month'])[['daily_avg']].mean()
    monthly_avg_temp.rename(columns = {'daily_avg':'Monthly mean temperature'},inplace = True)
    return monthly_avg_temp


@st.cache
def selecting_mean(monthly_avg_temp,option_mean):
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
    x = alt.X('Month:Q',scale = alt.Scale(domain=[1,12])),
    y = alt.Y('Monthly mean temperature:Q',scale = alt.Scale(domain=[12,35])),
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

    mean_chart = (points + lines).properties(width=1000, height=400).interactive()
    return mean_chart

def max_temp_plot(df_max,lat_long_val):
    fig_max = px.line(df_max,x = 'Year',y='Yearly_maximum_temp',title = 'Yearly Maximum Temperature')
    fig_max.update_traces(line_color = 'maroon')
    fig_max.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_max.update_xaxes(gridcolor='whitesmoke')
    fig_max.update_yaxes(gridcolor = 'whitesmoke')
    fig_max.update_layout(title = "Yearly Maximum Temperature: "+str(lat_long_val))

    return fig_max


def min_temp_plot(df_min,lat_long_val):
    fig_min = px.line(df_min, x= 'Year',y = 'Yearly_minimum_temp',title = 'Yearly Minimum Temperature')
    fig_min.update_traces(line_color ='blue')
    fig_min.update_layout(
    yaxis = dict(tickfont = dict(size=15)),
    xaxis = dict(tickfont = dict(size=15)),
    plot_bgcolor = 'rgba(0,0,0,0)')
    fig_min.update_xaxes(gridcolor='whitesmoke')
    fig_min.update_yaxes(gridcolor = 'whitesmoke')
    fig_min.update_layout(title = "Yearly Minimum Temperature: "+str(lat_long_val))

    return fig_min


#code for downloading Data as a CSV File
@st.cache
def convert_df(df):
     return df.to_csv().encode('utf-8')


#result dataframe contains the daily average value as well.
#Function for creating folium map and returning the latitude and Longitude of the clicked location
def map_creation(lat,long):
    with st.sidebar:
        with st.container():
            m = folium.Map(location = [8,38],zoom_start = 7)
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
            folium.Marker([lat,long],popup = "ET",tooltip='Ethopia').add_to(m)
            st_data = st_folium(m,key = 'map_fig_1')
            return st_data

#df is the initial df that contains only et data
def search_func(latitude,longitude,lt_lng_lst,df):
    if latitude and longitude in lt_lng_lst:
        st.write('Nearest Latitude and Longitude point is:',latitude +','+longitude)
    else:
        #implement haversine distance to calculate nearest Latitude, Longitude
        #_get_value is depricated in python
        df['lat_radian'],df['long_radian'] = np.radians(df['lat']),np.radians(df['long'])
        df['dLON'] = df['long_radian'] - math.radians(longitude)
        df['dLAT'] = df['lat_radian'] - math.radians(latitude)
        df['distance'] = 6371 * 2 * np.arcsin(np.sqrt(np.sin(df['dLAT']/2)**2 + math.cos(math.radians(longitude)) * np.cos(df['lat_radian']) * np.sin(df['dLON']/2)**2))
        a = df['distance'].idxmin()
        nearest_neighbor = df._get_value(a,'lat_long')
        st.write("**Nearest Latitude and Longitude is :**",nearest_neighbor)
        return nearest_neighbor


### Dashboard Creation
#creating the Sidebar Menu
with st.sidebar:
    temp_precp_selectbox = st.selectbox("Select the data type to view",('Temperature','Precipitation'))

    if temp_precp_selectbox == 'Temperature':
        #creating radio button
        data_type = st.radio("Select the data type to view the plot",
                        ('Daily Average','Monthly Mean Temperature','Annual Maximum Temperature','Annual Minimum Temperature','Annual Average Temperature','Annual Max, Min, & Average Temperature'))

    if temp_precp_selectbox == 'Precipitation':
        data_type = st.radio("Select the data type to view the plot",
                        ('Daily Average Precipitation','Monthly Average Precipitation','Annual Maximum Precipitation','Annual Minimum Precipitation','Annual Average Precipitation'))

#dividing the screen column into 2 sections for daily_average
if data_type == 'Daily Average':

    #streamlit code for selecting start and end date and plotting the data
    start = pd.to_datetime('2001/01/01')
    end = pd.to_datetime('2019/12/31')

    with  st.container():
        col1,col2 = st.columns(2)
        #creating dropdown menu for entering start and end date
        with col1:
            st.markdown('**Enter Start Date**')
            start = st.date_input("",value = start,key = 1)
            if start < pd.to_datetime('2001/01/01'):
                st.write('Start date should not be less than 2001/01/01')

            st.markdown('**Enter End Date**')
            end = st.date_input("",value = end, key = 2)
            if end > pd.to_datetime('2019/12/31'):
                st.write('End date should not be greater than 2019/12/31')
        #dropdown menu for selecting lat long values
        with col2:
            st.markdown('**Select the Latitude and Longitude**')
            option = st.selectbox("",pd.DataFrame(lat_long_list),key = 3)
            #for calling the map creation function
            lat  = float(option.split(',')[0])
            long = float(option.split(',')[1])
            m = map_creation(lat,long)
            last_click = m['last_clicked']
    #plotting the actual dropdown selected plot
    with st.container():
        dataframe_s_e = daily_avg_calc(result,option)
        fig = daily_avg_plot(dataframe_s_e,option)
        st.plotly_chart(fig,use_container_width = True)
        col11,col22,col33 = st.columns(3)

        with col22:
            st.download_button("Download Data",data = convert_df(dataframe_s_e),
                                file_name='daily_average_temperature.csv',
                                mime='text/csv',)

    #finding the clicked lat long and the nearest lat long
    with col2:
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            st.markdown("**Last Clicked Latitude Longitude point is:**")
            st.write(clicked_lat,clicked_long)
            nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
        else:
            st.markdown("**Click on the map to fetch the Latitude and Longitude**")
            st.markdown("   ")
            st.markdown("   ")

#plotting the nearest neighbors graph
    with st.container():
        if nn != 0 :
            df = daily_avg_calc(result,nn)
            fig_nn = daily_avg_plot(df,nn)
            st.plotly_chart(fig_nn,use_container_width = True)
            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",data = convert_df(df),
                                    file_name='daily_average_temperature_nn.csv',
                                    mime='text/csv',)


elif data_type == 'Monthly Mean Temperature':
    #creating the UI for selecting the year,lat long
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('**Select the Start Year**')
            start_year = st.selectbox('',
                                      ('2001','2002','2003','2004','2005','2006','2007','2008','2009',
                                      '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'),key = 4)

            st.markdown('**Select the End Year**')
            end_year = st.selectbox('',
                                      ('2001','2002','2003','2004','2005','2006','2007','2008','2009',
                                      '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'),key = 5)
        with col2:
            st.markdown('**Select the Latitude and Longitude**')
            option_mean = st.selectbox("",pd.DataFrame(lat_long_list),key = 6)



    #Finding the monthly mean/avg temperature
    temperature_monthly_df = result.copy()
    #function for calculating mean
    df_mean = monthly_mean_calc(temperature_monthly_df,lat_long_list)
    #function for selecting the specified group of lat long along with the start and end date
    df = selecting_mean(df_mean,option_mean)
    #function for plotting the mean data
    mean_chart = plot_mean_data(df,option_mean)
    mean_chart

    #for map
    lat_mean  = float(option_mean.split(',')[0])
    long_mean = float(option_mean.split(',')[1])

    with col2:
        m_mean = map_creation(lat_mean,long_mean)
        last_click = m_mean['last_clicked']
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            st.markdown("**Last Clicked Latitude Longitude point is:**")
            st.write(clicked_lat,clicked_long)
            nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
        else:
            st.markdown("**Click on the map to fetch the Latitude and Longitude**")
            st.markdown("   ")
            st.markdown("   ")


    col11,col22,col33 = st.columns(3)
    with col22:
        st.download_button("Download Data",data = convert_df(df),
                            file_name='Monthly_mean_temperature.csv',
                            mime='text/csv',)

        st.markdown("   ")

#code for plotting the nearest neighbors data
    with st.container():
        if nn != 0 :
            df_nn_mean = selecting_mean(df_mean,nn)
            fig_nn_mean = plot_mean_data(df_nn_mean,nn)
            fig_nn_mean
            col11,col22,col33 = st.columns(3)

            with col22:
                st.download_button("Download Data",data = convert_df(df_nn_mean),
                                    file_name='Monthly_mean_temperature_nn.csv',
                                    mime='text/csv',)


#code for annual maximum temperature
elif data_type == 'Annual Maximum Temperature':
    Annual_temp = result.copy()
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('**Select the Latitude and Longitude**.')
        option_annual_temp = st.selectbox("",pd.DataFrame(lat_long_list),key = 7)

    df_max = annual_max_plot(Annual_temp,option_annual_temp)
    fig_max = max_temp_plot(df_max,option_annual_temp)
    st.plotly_chart(fig_max, use_container_width=True)

    #For maps
    lat_annual_max  = float(option_annual_temp.split(',')[0])
    long_annual_max = float(option_annual_temp.split(',')[1])

    with col2:
        m_max = map_creation(lat_annual_max,long_annual_max)
        last_click = m_max['last_clicked']
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            st.markdown("**Last Clicked Latitude Longitude point is:**")
            st.write(clicked_lat,clicked_long)
            nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
        else:
            st.markdown("**Click on the map to fetch the Latitude and Longitude**")
            st.markdown("   ")
            st.markdown("   ")
    col11,col22,col33 = st.columns(3)
    with col22:
        st.download_button("Download Data",data = convert_df(df_max),
                            file_name='Annual_maximum_temperature.csv',
                            mime='text/csv',)

    with st.container():
        if nn!=0:
            df_max_temp_nn = annual_max_plot(Annual_temp,nn)
            fig_max_nn = max_temp_plot(df_max_temp_nn,nn)
            st.plotly_chart(fig_max_nn, use_container_width = True)

            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",data = convert_df(df_max_temp_nn),
                                    file_name='Annual_maximum_temperature_nn.csv',
                                    mime='text/csv',)


elif data_type == 'Annual Minimum Temperature':
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('**Select the Latitude and Longitude**.')
        option_annual_min_temp = st.selectbox("", pd.DataFrame(lat_long_list),key = 8)

    Annual_temp_min = result.copy()
    df_min = annual_min_plot(Annual_temp_min,option_annual_min_temp)
    fig_min = min_temp_plot(df_min,option_annual_min_temp)
    st.plotly_chart(fig_min,use_container_width = True)

    #For maps
    lat_min  = float(option_annual_min_temp.split(',')[0])
    long_min = float(option_annual_min_temp.split(',')[1])

    with col2:
        m_min = map_creation(lat_min,long_min)
        last_click = m_min['last_clicked']
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            st.markdown("**Last Clicked Latitude Longitude point is:**")
            st.write(clicked_lat,clicked_long)
            nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
        else:
            st.markdown("**Click on the map to fetch the Latitude and Longitude**")
            st.markdown("   ")
            st.markdown("   ")

    st.download_button("Download Data",data = convert_df(df_min),
                        file_name='Annual_minimum_temperature.csv',
                        mime='text/csv',)

    with st.container():
        if nn!=0:
            nn_min_temp_df = annual_min_plot(Annual_temp_min,nn)
            fig_min_nn = min_temp_plot(nn_min_temp_df,nn)
            st.plotly_chart(fig_min_nn, use_container_width = True)
            st.download_button("Download Data",data = convert_df(nn_min_temp_df),
                                file_name='Annual_minimum_temperature_nn.csv',
                                mime='text/csv',)


elif data_type == 'Annual Average Temperature':
    col1,col2 = st.columns(2)
    annual_avg_df = result.copy()

    with col1:
        st.markdown('**Select the Latitude and Longitude**')
        annual_avg_option = st.selectbox("",pd.DataFrame(lat_long_list),key = 9)
        annual_temp = annual_avg_plot(annual_avg_df,annual_avg_option)

    fig_avg = avg_temp_plot(annual_temp,annual_avg_option)
    st.plotly_chart(fig_avg,use_container_width = True)

    col11,col22,col33 = st.columns(3)
    with col22:
        st.download_button("Download Data",
                       data = convert_df(annual_temp),
                       file_name='Annual_average_temperature.csv',
                       mime='text/csv',)
#For maps
    lat_avg  = float(annual_avg_option.split(',')[0])
    long_avg = float(annual_avg_option.split(',')[1])

    with col2:
        m_avg = map_creation(lat_avg,long_avg)
        last_click = m_avg['last_clicked']
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            st.markdown("**Last Clicked Latitude Longitude point is:**")
            st.write(clicked_lat,clicked_long)
            nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
        else:
            st.markdown("**Click on the map to fetch the Latitude and Longitude**")

    with st.container():
        if nn!=0:
            nn_avg_temp_df = annual_avg_plot(annual_avg_df,nn)
            fig_avg_nn = avg_temp_plot(nn_avg_temp_df,nn)
            st.plotly_chart(fig_avg_nn, use_container_width = True)

            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",
                                data = convert_df(nn_avg_temp_df),
                                file_name='Annual_average_temperature_nn.csv',
                                mime='text/csv',)


elif data_type == 'Annual Max, Min, & Average Temperature':
        df = result.copy()
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('**Select the Latitude and Longitude**.')
            option_lat_long = st.selectbox("",pd.DataFrame(lat_long_list),key = 10)

        with col2:
            #For maps
            lat_avg_3  = float(option_lat_long.split(',')[0])
            long_avg_3 = float(option_lat_long.split(',')[1])
            m_max_min_avg = map_creation(lat_avg_3,long_avg_3)

            last_click = m_max_min_avg['last_clicked']
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.markdown(" ")
                st.markdown(" ")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")


        col1,col2,col3 = st.columns(3)
        with col1:
            with st.container():
                df1 = annual_max_plot(df,option_lat_long)
                fig_2 = max_temp_plot(df1,option_lat_long)
                st.plotly_chart(fig_2, use_container_width=True)

                st.download_button("Download Data",
                                data = convert_df(df1),
                                file_name='Annual_maximum_temperature.csv',
                                mime='text/csv',)

            with st.container():
                if nn!=0:
                    df_annual_max_2 = annual_max_plot(df,nn)
                    fig_annual_max_nn_2 = max_temp_plot(df_annual_max_2,nn)
                    st.plotly_chart(fig_annual_max_nn_2, use_container_width=True)
                    st.download_button("Download Data",
                                    data = convert_df(df_annual_max_2),
                                    file_name='Annual_maximum_temperature_nn.csv',
                                    mime='text/csv',)

        with col2:
            with st.container():
                df2 = annual_min_plot(df,option_lat_long)
                fig_3 = min_temp_plot(df2,option_lat_long)
                st.plotly_chart(fig_3,use_container_width = True)
                st.download_button("Download Data",
                                data = convert_df(df2),
                                file_name='Annual_minimum_temperature.csv',
                                mime='text/csv',)
            with st.container():
                if nn!=0:
                    df_annual_min_2 = annual_min_plot(df,nn)
                    fig_annual_min_nn_2 = min_temp_plot(df_annual_min_2,nn)
                    st.plotly_chart(fig_annual_min_nn_2, use_container_width=True)
                    st.download_button("Download Data",
                                    data = convert_df(df_annual_min_2),
                                    file_name='Annual_minimum_temperature_nn.csv',
                                    mime='text/csv',)
        with col3:
            with st.container():
                annual_average = annual_avg_plot(df,option_lat_long)
                fig_4 = avg_temp_plot(annual_average,option_lat_long)
                st.plotly_chart(fig_4,use_container_width = True)

                st.download_button("Download Data",
                                data = convert_df(annual_average),
                                file_name='Annual_average_temperature.csv',
                                mime='text/csv',)

            with st.container():
                if nn!=0:
                    df_annual_avg_nn_2 = annual_avg_plot(df,nn)
                    fig_nn_4 = avg_temp_plot(df_annual_avg_nn_2,nn)
                    st.plotly_chart(fig_nn_4,use_container_width=True)
                    st.download_button("Download Data",
                                    data = convert_df(df_annual_avg_nn_2),
                                    file_name='Annual_average_temperature_nn.csv',
                                    mime='text/csv',)
else:
    st.markdown("Work in Progress")
