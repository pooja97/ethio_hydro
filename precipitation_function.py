import pandas as pd
import numpy as np
import streamlit as st



#imports for finding the nearest lat long using haversine distance

#visualization libraries to visualize different plots
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import io

#for Logo plotting
from PIL import Image

#disabling warnings
import warnings
warnings.filterwarnings("ignore")

#For parallel processing
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)


@st.cache(allow_output_mutation=True)
def main_concat(a,b):
    z = pd.concat([a,b],ignore_index = True)
    return z



@st.cache
def date_split(df):
    df[['Year','Month','Day']] = df['date'].str.split('-',expand = True)
    return df


@st.cache(allow_output_mutation = True)
def lat_long_process_precp(df):
    df['lat_long'] = df['lat'].astype(str)+','+df['long'].astype(str)
    return df



@st.cache
def drop_dup_funct(x):
    x.drop_duplicates(inplace = True)
    return x

@st.cache(allow_output_mutation = True)
def concat_func(x,y,a,b):
    z = pd.concat([x,y,a,b],ignore_index = True)
    return z

@st.cache
def lat_long_type(nn_value):
    if isinstance(nn_value,str):
        return nn_value
    else:
        return nn_value.item((0))

@st.cache
def cumulative(df,start,end):
    df1 = df.groupby(['Year','Month'])['precip'].sum()
    df1 = df1.reset_index()
    df1 = df1.set_index('Year')
    df1 = df1.loc[str(start):str(end)]
    return df1

@st.cache
def cumulative_plot(df):
    fig  = px.line(df, y='precip',title = 'Monthly Cumulative Precipitation')
    fig.update_traces(line_color = 'blue')
    fig.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig.update_yaxes(ticklabelposition="inside top", title= 'Monthly Cumulative Precipitation in mm',gridcolor = 'whitesmoke')
    fig.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_layout(title = "Monthly Cumulative Precipitation")
    return fig


@st.cache(allow_output_mutation=True)
def daily_precp_data(precipitation_temp,start,end,option):
    df_daily = precipitation_temp.get_group(option)
    df_daily.set_index('date',inplace = True)
    # df_2 = df_daily.loc[str(start):str(end)]
    # df_3=df_2.reset_index()
    return df_daily

@st.cache
def daily_precp_plot(df):
    fig  = px.line(df,y='precip',title = 'Daily Precipitation')
    fig.update_traces(line_color = 'blue')
    fig.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig.update_yaxes(ticklabelposition="inside top", title= 'Daily Precipitation in mm',gridcolor = 'whitesmoke')
    fig.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_layout(title = "Daily Precipitation")
    return fig

def start_end_date_ui(start,end,key1,key2):
    st.markdown('**Enter Start Date**')
    start = st.date_input("",value = start,key = key1)
    if start < pd.to_datetime('2001/01/01'):
        st.write('Start date should not be less than 2001/01/01')

    st.markdown('**Enter End Date**')
    end = st.date_input("",value = end, key = key2)
    if end > pd.to_datetime('2019/12/31'):
        st.write('End date should not be greater than 2019/12/31')
    return start,end


def lat_long_ui(key1,key2):
    st.markdown('**Enter the latitude**')
    latitude_input = st.text_input('','12.55',key = key1)
    st.markdown('**Enter the longitude**')
    longitude_input = st.text_input('','42.45',key = key2)
    return latitude_input,longitude_input


def year_selection_ui(key1,key2):
    st.markdown('**Select the Start Year**')
    start_year = st.selectbox('',
                              ('2001','2002','2003','2004','2005','2006','2007','2008','2009',
                              '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'),key = key1)

    st.markdown('**Select the End Year**')
    end_year = st.selectbox('',
                              ('2001','2002','2003','2004','2005','2006','2007','2008','2009',
                              '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'),key = key2)

    return start_year,end_year

@st.cache(allow_output_mutation=True)
def monthly_mean_plot(df):
    title_text = "Monthly Mean Precipitation"
    highlight = alt.selection(
    type='single', on='mouseover', fields=['Year'], nearest=True)
    base = alt.Chart(df,title = title_text).encode(
    x = alt.X('Month:Q',scale = alt.Scale(domain=[1,12]),axis=alt.Axis(tickMinStep=1)),
    y = alt.Y('precip:Q',scale = alt.Scale(domain=[df['precip'].min(),df['precip'].max()])),
    color = alt.Color('Year:O',scale = alt.Scale(scheme = 'magma'))
    )
    points = base.mark_circle().encode(
    opacity=alt.value(0),
    tooltip=[
        alt.Tooltip('Year:O', title='Year'),
        alt.Tooltip('Month:Q', title='Month'),
        alt.Tooltip('precip:Q', title='Monthly Mean Precipitation')
    ]).add_selection(highlight)

    lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3)))

    mean_chart = (points + lines).properties(width=1000, height=400).interactive()
    return mean_chart

@st.cache
def annual_max_precip_plot(df):
    fig_max  = px.line(df, x = 'Year',y='precip',title = 'Annual Maximum Precipitation')
    fig_max.update_traces(line_color = 'maroon')
    fig_max.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig_max.update_yaxes(ticklabelposition="inside top", title= 'Annual Maximum Precipitation in mm',gridcolor = 'whitesmoke')
    fig_max.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig_max.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig_max.update_layout(title = "Annual Maximum Precipitation")
    return fig_max


def annual_min_precip_plot(df):
    fig_min  = px.line(df, x = 'Year',y='precip',title = 'Annual Minimum Precipitation')
    fig_min.update_traces(line_color = 'blue')
    fig_min.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig_min.update_yaxes(ticklabelposition="inside top", title= 'Annual Minimum Precipitation in mm',gridcolor = 'whitesmoke')
    fig_min.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig_min.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig_min.update_layout(title = "Annual Minimum Precipitation")
    return fig_min

def annual_avg_plot(df):
    fig_avg  = px.line(df, x = 'Year',y='precip',title = 'Annual Average Precipitation')
    fig_avg.update_traces(line_color = 'dimgray')
    fig_avg.update_xaxes(title_text = 'Year',gridcolor = 'whitesmoke')
    fig_avg.update_yaxes(ticklabelposition="inside top", title= 'Annual Average Precipitation in mm',gridcolor = 'whitesmoke')
    fig_avg.update_layout(margin = dict(l=25,r=25,t=25,b=25))
    fig_avg.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    fig_avg.update_layout(title = "Annual Average Precipitation")
    return fig_avg


@st.cache
def max_precip(precipitation_temp,option,start_year,end_year):
    maximum_precip_df = precipitation_temp.get_group(option)
    maximum_precip_df = date_split(maximum_precip_df)
    Annual_max_precip = maximum_precip_df.groupby('Year')['precip'].max()
    Annual_max_precip = Annual_max_precip.loc[str(start_year):str(end_year)]
    Annual_max_precip = Annual_max_precip.reset_index()
    return Annual_max_precip

@st.cache
def min_precip(precipitation_temp,option,start_year,end_year):
    minimum_precip_df = precipitation_temp.get_group(option)
    minimum_precip_df = date_split(minimum_precip_df)
    minimum_precip_df = minimum_precip_df.where(minimum_precip_df['precip']>0)
    minimum_precip_df = minimum_precip_df.groupby('Year')['precip'].min()
    minimum_precip_df = minimum_precip_df.loc[str(start_year):str(end_year)]
    minimum_precip_df = minimum_precip_df.reset_index()
    return minimum_precip_df

@st.cache
def avg_precip(precipitation_temp,option,start_year,end_year):
    avg_precip_df = precipitation_temp.get_group(option)
    avg_precip_df = date_split(avg_precip_df)
    avg_precip_df = avg_precip_df.groupby('Year')['precip'].mean()
    avg_precip_df_s_e = avg_precip_df.loc[str(start_year):str(end_year)]
    avg_precip_df_s_e = avg_precip_df_s_e.reset_index()
    return avg_precip_df_s_e
