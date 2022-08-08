import pandas as pd
import numpy as np
import streamlit as st
import folium
import folium.plugins

from streamlit_folium import st_folium
from branca.element import Figure


from precipitation_function import date_split,lat_long_process_precp
from precipitation_function import concat_func, drop_dup_funct,lat_long_type
from precipitation_function import daily_precp_plot,start_end_date_ui,lat_long_ui,year_selection_ui
from precipitation_function import monthly_mean_plot, annual_max_precip_plot,daily_precp_data,cumulative_plot
from precipitation_function import annual_max_precip_plot,annual_min_precip_plot,annual_avg_plot,max_precip,min_precip,avg_precip,cumulative,main_concat

from temperature_functions import convert_df, map_creation, search_func

def run():
    fig = Figure(width = 550,height = 350)

    nearest_lat_long = 0
    nn = 0
    start = pd.to_datetime('2001/01/01')
    end = pd.to_datetime('2019/12/31')


    precipitation_1_og = pd.read_csv('historicalData/precip1.zip',compression = 'zip')
    precipitation_2_og = pd.read_csv('historicalData/precip2.zip',compression = 'zip')
    precipitation_3_og = pd.read_csv('historicalData/precip3.zip',compression = 'zip')
    precipitation_4_og = pd.read_csv('historicalData/precip4.zip',compression = 'zip')
    precipitation_5_og = pd.read_csv('historicalData/precip5.zip',compression = 'zip')
    precipitation_6_og = pd.read_csv('historicalData/precip6.zip',compression = 'zip')
    precipitation_7_og = pd.read_csv('historicalData/precip7.zip',compression = 'zip')
    precipitation_8_og = pd.read_csv('historicalData/precip8.zip',compression = 'zip')
    # precipitation_9_og = pd.read_csv('historicalData/precip9.zip',compression = 'zip')
    # precipitation_10_og = pd.read_csv('historicalData/precip10.zip',compression = 'zip')
    # precipitation_11_og = pd.read_csv('historicalData/precip11.zip',compression = 'zip')
    # precipitation_12_og = pd.read_csv('historicalData/precip12.zip',compression = 'zip')
    # precipitation_13_og = pd.read_csv('historicalData/precip13.zip',compression = 'zip')
    # precipitation_14_og = pd.read_csv('historicalData/precip14.zip',compression = 'zip')
    # precipitation_15_og = pd.read_csv('historicalData/precip15.zip',compression = 'zip')
    # precipitation_16_og = pd.read_csv('historicalData/precip16.zip',compression = 'zip')


    lat_long_precipitation_1 = precipitation_1_og['lat_long']
    lat_long_precipitation_2 = precipitation_2_og['lat_long']
    lat_long_precipitation_3 = precipitation_3_og['lat_long']
    lat_long_precipitation_4 = precipitation_4_og['lat_long']
    lat_long_precipitation_5 = precipitation_5_og['lat_long']
    lat_long_precipitation_6 = precipitation_6_og['lat_long']
    lat_long_precipitation_7 = precipitation_7_og['lat_long']
    lat_long_precipitation_8 = precipitation_8_og['lat_long']
    # lat_long_precipitation_9 = precipitation_9_og['lat_long']
    # lat_long_precipitation_10 = precipitation_10_og['lat_long']
    # lat_long_precipitation_11 = precipitation_11_og['lat_long']
    # lat_long_precipitation_12 = precipitation_12_og['lat_long']
    # lat_long_precipitation_13 = precipitation_13_og['lat_long']
    # lat_long_precipitation_14 = precipitation_14_og['lat_long']
    # lat_long_precipitation_15 = precipitation_15_og['lat_long']
    # lat_long_precipitation_16 = precipitation_16_og['lat_long']



    lat_long_precipitation_list_1 = concat_func(lat_long_precipitation_1,lat_long_precipitation_2,lat_long_precipitation_3,lat_long_precipitation_4)
    lat_long_precipitation_list_2 = concat_func(lat_long_precipitation_5,lat_long_precipitation_6,lat_long_precipitation_7,lat_long_precipitation_8)
    # lat_long_precipitation_list_3 = concat_func(lat_long_precipitation_9,lat_long_precipitation_10,lat_long_precipitation_11,lat_long_precipitation_12)

    # lat_long_precipitation_list_4 = concat_func(lat_long_precipitation_13,lat_long_precipitation_14,lat_long_precipitation_15,lat_long_precipitation_16)
    lat_long_precipitation_list   = main_concat(lat_long_precipitation_list_1,lat_long_precipitation_list_2)


    precipitation_conc_1 = concat_func(precipitation_1_og,precipitation_2_og,precipitation_3_og,precipitation_4_og)
    precipitation_conc_2 = concat_func(precipitation_5_og,precipitation_6_og,precipitation_7_og,precipitation_8_og)
    # precipitation_conc_3 = concat_func(precipitation_9_og,precipitation_10_og,precipitation_11_og,precipitation_12_og)
    # precipitation_conc_4 = concat_func(precipitation_13_og,precipitation_14_og,precipitation_15_og,precipitation_16_og)
    precipitation = main_concat(precipitation_conc_1,precipitation_conc_2)

    # precipitation = precipitation.drop([Unnamed:0.2,Unnamed:0.1,Unnamed:0],axis =1)
    precipitation.drop(precipitation.filter(regex="Unnamed"),axis=1, inplace=True)
    # st.write(precipitation.head())
    precipitation_temp = precipitation.copy()
    precipitation_temp = precipitation_temp.groupby('lat_long')

    with st.sidebar:
        data_type = st.radio("Select Data Type to View",
                        ('Daily Precipitation','Cumulative Monthly Precipitation','Monthly Average Precipitation',
                        'Annual Maximum Precipitation','Annual Minimum Precipitation',
                        'Annual Average Precipitation','Annual Max, Min, & Average Precipitation'))

    if data_type == "Cumulative Monthly Precipitation":
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(99,100)
        with col2:
            #calling the ui method to create a lat long input UI
            latitude_input,longitude_input = lat_long_ui(300,400)


        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        df_cumulative = precipitation_temp.get_group(option)
        df_cumulative = date_split(df_cumulative)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)
        last_click = m['last_clicked']

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)

        df_c = cumulative(df_cumulative,start_year,end_year)
        fig_cumulative = cumulative_plot(df_c)
        st.plotly_chart(fig_cumulative,use_container_width=True)
        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(df_c),
                                file_name='cumulative_precipitation.csv',
                                mime='text/csv',)


    elif data_type == "Daily Precipitation":
        col1,col2 = st.columns(2)
        with col1:
            #calling the ui method to create a start end date input UI
            start,end = start_end_date_ui(start,end,11,22)
        with col2:
            latitude_input,longitude_input = lat_long_ui(1,2)


        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)


        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)
        last_click = m['last_clicked']

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)


        daily_precp_df = daily_precp_data(precipitation_temp,start,end,option)
        # st.write(daily_precp_df.head())
        daily_precp_df.drop_duplicates(inplace = True)
        daily_df = daily_precp_df.loc[str(start):str(end)]
        # st.write(daily_df)
        fig_daily_precp = daily_precp_plot(daily_df)
        st.plotly_chart(fig_daily_precp,use_container_width = True)

        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(daily_precp_df),
                                file_name='daily_precipitation.csv',
                                mime='text/csv',)


    elif data_type == 'Monthly Average Precipitation':
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(9,10)
        with col2:
            #calling the ui method to create a lat long input UI
            latitude_input,longitude_input = lat_long_ui(3,4)

        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)

        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)


        precipitation_monthly_avg = precipitation_temp.get_group(option)
        precipitation_monthly_avg = date_split(precipitation_monthly_avg)
        precipt_monthly_avg_df = precipitation_monthly_avg.groupby(['Year','Month'],as_index=False)['precip'].mean()
        precipt_monthly_avg_df = precipt_monthly_avg_df.set_index('Year')
        precipitation_monthly_avg_df = precipt_monthly_avg_df.loc[str(start_year):str(end_year)]
        precipitation_monthly_avg_df.reset_index(inplace = True)
        mean_chart_plot = monthly_mean_plot(precipitation_monthly_avg_df)
        st.altair_chart(mean_chart_plot)


        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(precipitation_monthly_avg_df),
                                file_name='Monthly_avg_precipitation.csv',
                                mime='text/csv',)


    elif data_type == 'Annual Maximum Precipitation':
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(11,12)
        with col2:
            #calling the ui method to create a lat long input UI
            latitude_input,longitude_input = lat_long_ui(5,6)

        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)

        Annual_max_precip = max_precip(precipitation_temp,option,start_year,end_year)
        fig_max = annual_max_precip_plot(Annual_max_precip)
        st.plotly_chart(fig_max,use_container_width=True)

        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(Annual_max_precip),
                                file_name='Annual_max_precipitation.csv',
                                mime='text/csv',)


    elif data_type == 'Annual Minimum Precipitation':
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(13,14)
        with col2:
            #calling the ui method to create a lat long input UI
            latitude_input,longitude_input = lat_long_ui(7,8)

        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)


        minimum_precip_df = min_precip(precipitation_temp,option,start_year,end_year)
        fig_min = annual_min_precip_plot(minimum_precip_df)
        st.plotly_chart(fig_min,use_container_width = True)


        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(minimum_precip_df),
                                file_name='Annual_minimum_precipitation.csv',
                                mime='text/csv',)



    elif data_type == 'Annual Average Precipitation':
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(15,16)
        with col2:
            #calling the ui method to create a lat long input UI
            latitude_input,longitude_input = lat_long_ui(9,10)

        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)

        avg_precip_df_se = avg_precip(precipitation_temp,option,start_year,end_year)
        fig_avg = annual_avg_plot(avg_precip_df_se)
        st.plotly_chart(fig_avg,use_container_width = True)

        c1,c2,c3,c4,c5 = st.columns(5)
        with c3:
            st.download_button("Download Data",data = convert_df(avg_precip_df_se),
                                file_name='Annual_avg_precipitation.csv',
                                mime='text/csv',)

    elif data_type == 'Annual Max, Min, & Average Precipitation':
        col1,col2 = st.columns(2)
        with col1:
            start_year,end_year = year_selection_ui(17,18)

        with col2:
            latitude_input,longitude_input = lat_long_ui(11,12)

        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        option = lat_long_type(nearest_lat_long)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long,0,0)

        last_click = m['last_clicked']
        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                map_creation(lat,long,clicked_lat,clicked_long)

        col11,col22,col33 = st.columns(3)
        with col11:
            annual_max_data = max_precip(precipitation_temp,option,start_year,end_year)
            fig_max_2 = annual_max_precip_plot(annual_max_data)
            st.plotly_chart(fig_max_2,use_container_width=True)
            st.download_button("Download Data",data = convert_df(annual_max_data),
                                file_name='Annual_max_precipitation_data.csv',
                                mime='text/csv',)

        with col22:
            annual_min_data = min_precip(precipitation_temp,option,start_year,end_year)
            fig_min_2 = annual_min_precip_plot(annual_min_data)
            st.plotly_chart(fig_min_2,use_container_width = True)
            st.download_button("Download Data",data = convert_df(annual_min_data),
                                file_name='Annual_min_precipitation_data.csv',
                                mime='text/csv',)

        with col33:
            annual_avg_data = avg_precip(precipitation_temp,option,start_year,end_year)
            fig_avg_2 = annual_avg_plot(annual_avg_data)
            st.plotly_chart(fig_avg_2, use_container_width = True)
            st.download_button("Download Data",data = convert_df(annual_avg_data),
                                file_name='Annual_avg_precipitation_data.csv',
                                mime='text/csv',)


if __name__ == 'main':
    run()
