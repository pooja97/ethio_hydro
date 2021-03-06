import pandas as pd
import numpy as np
import streamlit as st


from precipitation_function import date_split,lat_long_process_precp
from precipitation_function import concat_func, drop_dup_funct,lat_long_type
from precipitation_function import daily_precp_plot,start_end_date_ui,lat_long_ui,year_selection_ui
from precipitation_function import monthly_mean_plot, annual_max_precip_plot,daily_precp_data,read_file
from precipitation_function import annual_max_precip_plot,annual_min_precip_plot,annual_avg_plot,max_precip,min_precip,avg_precip

from temperature_functions import convert_df, map_creation, search_func

def run():
    nearest_lat_long = 0
    nn = 0
    start = pd.to_datetime('2001/01/01')
    end = pd.to_datetime('2019/12/31')

    #precipitation data
    bucket_name = "timeseries_data_storage"
    file_path_1 = "precip_data/precip1.zip"
    file_path_2 = "precip_data/precip2.zip"
    file_path_3 = "precip_data/precip3.zip"
    file_path_4 = "precip_data/precip4.zip"
    file_path_5 = "precip_data/precip5.zip"
    file_path_6 = "precip_data/precip6.zip"
    file_path_7 = "precip_data/precip7.zip"
    file_path_8 = "precip_data/precip8.zip"
    file_path_9 = "precip_data/precip9.zip"
    file_path_10 = "precip_data/precip10.zip"
    file_path_11 = "precip_data/precip11.zip"
    file_path_12 = "precip_data/precip12.zip"
    file_path_13 = "precip_data/precip13.zip"
    file_path_14 = "precip_data/precip14.zip"
    file_path_15 = "precip_data/precip15.zip"
    file_path_16 = "precip_data/precip16.zip"



    precipitation_1_og = read_file(bucket_name,file_path_1)
    precipitation_2_og = read_file(bucket_name,file_path_2)
    precipitation_3_og = read_file(bucket_name,file_path_3)
    precipitation_4_og = read_file(bucket_name,file_path_4)
    precipitation_5_og = read_file(bucket_name,file_path_5)
    precipitation_6_og = read_file(bucket_name,file_path_6)
    precipitation_7_og = read_file(bucket_name,file_path_7)
    precipitation_8_og = read_file(bucket_name,file_path_8)
    precipitation_9_og = read_file(bucket_name,file_path_9)
    precipitation_10_og = read_file(bucket_name,file_path_10)
    precipitation_11_og = read_file(bucket_name,file_path_11)
    precipitation_12_og = read_file(bucket_name,file_path_12)
    precipitation_13_og = read_file(bucket_name,file_path_13)
    precipitation_14_og = read_file(bucket_name,file_path_14)
    precipitation_15_og = read_file(bucket_name,file_path_15)
    precipitation_16_og = read_file(bucket_name,file_path_16)


    precipitation_1_lst = lat_long_process_precp(precipitation_1_og)
    precipitation_2_lst = lat_long_process_precp(precipitation_2_og)
    precipitation_3_lst = lat_long_process_precp(precipitation_3_og)
    precipitation_4_lst = lat_long_process_precp(precipitation_4_og)
    precipitation_5_lst = lat_long_process_precp(precipitation_5_og)
    precipitation_6_lst = lat_long_process_precp(precipitation_6_og)
    precipitation_7_lst = lat_long_process_precp(precipitation_7_og)
    precipitation_8_lst = lat_long_process_precp(precipitation_8_og)
    precipitation_9_lst = lat_long_process_precp(precipitation_9_og)
    precipitation_10_lst = lat_long_process_precp(precipitation_10_og)
    precipitation_11_lst = lat_long_process_precp(precipitation_11_og)
    precipitation_12_lst = lat_long_process_precp(precipitation_12_og)
    precipitation_13_lst = lat_long_process_precp(precipitation_13_og)
    precipitation_14_lst = lat_long_process_precp(precipitation_14_og)
    precipitation_15_lst = lat_long_process_precp(precipitation_15_og)
    precipitation_16_lst = lat_long_process_precp(precipitation_16_og)




    precipitation_1_lst = drop_dup_funct(precipitation_1_lst)
    precipitation_2_lst = drop_dup_funct(precipitation_2_lst)
    precipitation_3_lst = drop_dup_funct(precipitation_3_lst)
    precipitation_4_lst = drop_dup_funct(precipitation_4_lst)
    precipitation_5_lst = drop_dup_funct(precipitation_5_lst)
    precipitation_6_lst = drop_dup_funct(precipitation_6_lst)
    precipitation_7_lst = drop_dup_funct(precipitation_7_lst)
    precipitation_8_lst = drop_dup_funct(precipitation_8_lst)
    precipitation_9_lst = drop_dup_funct(precipitation_9_lst)
    precipitation_10_lst = drop_dup_funct(precipitation_10_lst)
    precipitation_11_lst = drop_dup_funct(precipitation_11_lst)
    precipitation_12_lst = drop_dup_funct(precipitation_12_lst)
    precipitation_13_lst = drop_dup_funct(precipitation_13_lst)
    precipitation_14_lst = drop_dup_funct(precipitation_14_lst)
    precipitation_15_lst = drop_dup_funct(precipitation_15_lst)
    precipitation_16_lst = drop_dup_funct(precipitation_16_lst)



    lat_long_precipitation_1 = precipitation_1_lst['lat_long']
    lat_long_precipitation_2 = precipitation_2_lst['lat_long']
    lat_long_precipitation_3 = precipitation_3_lst['lat_long']
    lat_long_precipitation_4 = precipitation_4_lst['lat_long']
    lat_long_precipitation_5 = precipitation_5_lst['lat_long']
    lat_long_precipitation_6 = precipitation_6_lst['lat_long']
    lat_long_precipitation_7 = precipitation_7_lst['lat_long']
    lat_long_precipitation_8 = precipitation_8_lst['lat_long']
    lat_long_precipitation_9 = precipitation_9_lst['lat_long']
    lat_long_precipitation_10 = precipitation_10_lst['lat_long']
    lat_long_precipitation_11 = precipitation_11_lst['lat_long']
    lat_long_precipitation_12 = precipitation_12_lst['lat_long']
    lat_long_precipitation_13 = precipitation_13_lst['lat_long']
    lat_long_precipitation_14 = precipitation_14_lst['lat_long']
    lat_long_precipitation_15 = precipitation_15_lst['lat_long']
    lat_long_precipitation_16 = precipitation_16_lst['lat_long']



    lat_long_precipitation_list_1 = concat_func(lat_long_precipitation_1,lat_long_precipitation_2,lat_long_precipitation_3,lat_long_precipitation_4)
    lat_long_precipitation_list_2 = concat_func(lat_long_precipitation_5,lat_long_precipitation_6,lat_long_precipitation_7,lat_long_precipitation_8)
    lat_long_precipitation_list_3 = concat_func(lat_long_precipitation_9,lat_long_precipitation_10,lat_long_precipitation_11,lat_long_precipitation_12)
    lat_long_precipitation_list_4 = concat_func(lat_long_precipitation_13,lat_long_precipitation_14,lat_long_precipitation_15,lat_long_precipitation_16)
    lat_long_precipitation_list   = concat_func(lat_long_precipitation_list_1,lat_long_precipitation_list_2,lat_long_precipitation_list_3,lat_long_precipitation_list_4)



    precipitation_conc_1 = concat_func(precipitation_1_lst,precipitation_2_lst,precipitation_3_lst,precipitation_4_lst)
    precipitation_conc_2 = concat_func(precipitation_5_lst,precipitation_6_lst,precipitation_7_lst,precipitation_8_lst)
    precipitation_conc_3 = concat_func(precipitation_9_lst,precipitation_10_lst,precipitation_11_lst,precipitation_12_lst)
    precipitation_conc_4 = concat_func(precipitation_13_lst,precipitation_14_lst,precipitation_15_lst,precipitation_16_lst)
    precipitation = concat_func(precipitation_conc_1,precipitation_conc_2,precipitation_conc_3,precipitation_conc_4)



    precipitation_temp = precipitation.copy()
    precipitation_temp = precipitation_temp.groupby('lat_long')



    with st.sidebar:
        data_type = st.radio("Select Data Type to View",
                        ('Daily Precipitation','Monthly Average Precipitation',
                        'Annual Maximum Precipitation','Annual Minimum Precipitation',
                        'Annual Average Precipitation','Annual Max, Min, & Average Precipitation'))

    if data_type == "Daily Precipitation":
        col1,col2 = st.columns(2)
        with col1:
            #calling the ui method to create a start end date input UI
            start,end = start_end_date_ui(start,end,11,22)
        with col2:
            latitude_input,longitude_input = lat_long_ui(1,2)


        latitude_input,longitude_input= float(latitude_input),float(longitude_input)
        nearest_lat_long = search_func(latitude_input,longitude_input,lat_long_precipitation_list,precipitation)
        # st.write(type(nearest_lat_long))
        option = lat_long_type(nearest_lat_long)

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        df = precipitation_temp.get_group(option)
        df = date_split(df)

        lat  = float(option.split(',')[0])
        long = float(option.split(',')[1])
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        daily_precp_df = daily_precp_data(df,start,end)
        fig_daily_precp = daily_precp_plot(daily_precp_df)
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
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")


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
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

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
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")


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
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

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
        m = map_creation(lat,long)
        last_click = m['last_clicked']

        with col1:
            st.write("**Nearest latitude and longitude from the entered latitude longitude is :**",option)

        with col2:
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write(clicked_lat,clicked_long)
                nn = search_func(clicked_lat,clicked_long,lat_long_precipitation_list,precipitation)
                nn = lat_long_type(nn)
                st.write("**Nearest Latitude and Longitude is:**",nn)
                st.markdown(" ")
            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")

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
