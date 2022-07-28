

#standard imports
import pandas as pd
import numpy as np
import streamlit as st
import swifter
swifter.register_modin()
from typing import Dict, List, Optional

from temperature_functions import annual_avg, df_date_split, lat_long_process,lat_long_list_creation
from temperature_functions import group_df, daily_avg, annual_avg_plot, avg_temp_plot, annual_min_plot, annual_max_plot
from temperature_functions import daily_avg_calc, daily_avg_plot, monthly_mean_calc, selecting_mean, plot_mean_data, max_temp_plot
from temperature_functions import min_temp_plot, convert_df, map_creation, search_func
import folium
from streamlit_folium import st_folium
from branca.element import Figure



import warnings
warnings.filterwarnings("ignore")

#For parallel processing
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)



def run():

    #nearest neighbor
    nn = 0
    # bucket_name = 'timeseries_data_storage'
    # file_path1 = 'temperature1.zip'
    # file_path2 = 'temperature2.zip'
    tempe1 = pd.read_csv('historicalData/temperature1.csv')
    tempe2 = pd.read_csv('historicalData/temperature2.csv')
    temperatureDF = pd.concat([tempe1,tempe2],axis =0 )

    #creating copy of our dataframe
    temperatureDataFrame = temperatureDF.copy()

    #applying the function on the dataframe
    temperatureDataFrame = lat_long_process(temperatureDataFrame)

    #applying the lat long creation function on the dataframe
    lat_long_list = lat_long_list_creation(temperatureDataFrame)

    #applying the function on the dataframe
    result = group_df(temperatureDataFrame,lat_long_list)

    #Dataframe containing daily average
    result['daily_avg'] = result.swifter.apply(lambda x: daily_avg(x.tmin,x.tmax),axis=1)


    ### Dashboard Creation
    #creating the Sidebar Menu
    with st.sidebar.empty():
        with st.container():
            data_type = st.radio("Select Data Type to View",
                ('Daily Average','Monthly Mean Temperature','Annual Maximum Temperature','Annual Minimum Temperature','Annual Average Temperature','Annual Max, Min, & Average Temperature'))

    #dividing the screen column into 2 sections for daily_average
    if data_type == 'Daily Average':
        ab = st.empty()
        a = st.empty()
        b = st.empty()

        start = pd.to_datetime('2001/01/01')
        end = pd.to_datetime('2019/12/31')

        with  ab:
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
                lat  = float(option.split(',')[0])
                long = float(option.split(',')[1])
                m = map_creation(lat,long,0,0)
                last_click = m['last_clicked']
        with a:
            dataframe_s_e = daily_avg_calc(result,option,start,end)
            fig = daily_avg_plot(dataframe_s_e,option)
            st.plotly_chart(fig,use_container_width = True)
        with b:
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
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                st.write("**Nearest Latitude and Longitude is:**",nn)

            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")
                st.markdown("   ")
                st.markdown("   ")
        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat,long,clicked_lat,clicked_long)


    #plotting the nearest neighbors graph
        if nn != 0 :
            df = daily_avg_calc(result,nn,start,end)
            fig_nn = daily_avg_plot(df,nn)
            with a:
                st.plotly_chart(fig_nn,use_container_width = True)
            with b:
                col11,col22,col33 = st.columns(3)
                with col22:
                    st.download_button("Download Data",data = convert_df(df),
                                        file_name='daily_average_temperature_nn.csv',
                                        mime='text/csv',)


    elif data_type == 'Monthly Mean Temperature':
        #creating the UI for selecting the year,lat long
        c = st.empty()
        d = st.empty()
        e = st.empty()
        with c:
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
        df = selecting_mean(df_mean,option_mean,start_year,end_year)
        #function for plotting the mean data
        mean_chart = plot_mean_data(df,option_mean)
        with d:
            st.altair_chart(mean_chart)

        #for map
        lat_mean  = float(option_mean.split(',')[0])
        long_mean = float(option_mean.split(',')[1])

        with col2:
            m_mean = map_creation(lat_mean,long_mean,0,0)
            last_click = m_mean['last_clicked']
            if last_click is not None:
                clicked_lat = last_click['lat']
                clicked_long = last_click['lng']
                st.markdown("**Last Clicked Latitude Longitude point is:**")
                st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                st.write("**Nearest Latitude and Longitude is:**",nn)


            else:
                st.markdown("**Click on the map to fetch the Latitude and Longitude**")
                st.markdown("   ")
                st.markdown("   ")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat_mean,long_mean,clicked_lat,clicked_long)

        with e:
            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",data = convert_df(df),
                                    file_name='Monthly_mean_temperature.csv',
                                    mime='text/csv',)

                st.markdown("   ")

    #code for plotting the nearest neighbors data

        if nn != 0 :
            df_nn_mean = selecting_mean(df_mean,nn,start_year,end_year)
            fig_nn_mean = plot_mean_data(df_nn_mean,nn)
            with d:
                st.altair_chart(fig_nn_mean)
            with e:
                col11,col22,col33 = st.columns(3)
                with col22:
                    st.download_button("Download Data",data = convert_df(df_nn_mean),
                                            file_name='Monthly_mean_temperature_nn.csv',
                                            mime='text/csv',)

    #code for annual maximum temperature
    elif data_type == 'Annual Maximum Temperature':
        g = st.empty()
        h = st.empty()
        i = st.empty()
        Annual_temp = result.copy()
        with g:
            col1,col2 = st.columns(2)
            with col1:
                st.markdown('**Select the Latitude and Longitude**.')
                option_annual_temp = st.selectbox("",pd.DataFrame(lat_long_list),key = 7)

        df_max = annual_max_plot(Annual_temp,option_annual_temp,lat_long_list)
        fig_max = max_temp_plot(df_max,option_annual_temp)
        with h:
            st.plotly_chart(fig_max, use_container_width=True)

        #For maps
        lat_annual_max  = float(option_annual_temp.split(',')[0])
        long_annual_max = float(option_annual_temp.split(',')[1])

        with g:
            with col2:
                m_max = map_creation(lat_annual_max,long_annual_max,0,0)
                last_click = m_max['last_clicked']
                if last_click is not None:
                    clicked_lat = last_click['lat']
                    clicked_long = last_click['lng']
                    st.markdown("**Last Clicked Latitude Longitude point is:**")
                    st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                    nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                    st.write("**Nearest Latitude and Longitude is:**",nn)
                else:
                    st.markdown("**Click on the map to fetch the Latitude and Longitude**")
                    st.markdown("   ")
                    st.markdown("   ")

        if last_click is not None:
            clicked_lat = last_click['lat']
            clicked_long = last_click['lng']
            map_creation(lat_annual_max,long_annual_max,clicked_lat,clicked_long)
        with i:
            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",data = convert_df(df_max),
                                    file_name='Annual_maximum_temperature.csv',
                                    mime='text/csv',)

        with st.container():
            if nn!=0:
                df_max_temp_nn = annual_max_plot(Annual_temp,nn,lat_long_list)
                fig_max_nn = max_temp_plot(df_max_temp_nn,nn)
                with h:
                    st.plotly_chart(fig_max_nn, use_container_width = True)
                with i:
                    col11,col22,col33 = st.columns(3)
                    with col22:
                        st.download_button("Download Data",data = convert_df(df_max_temp_nn),
                                            file_name='Annual_maximum_temperature_nn.csv',
                                            mime='text/csv',)


    elif data_type == 'Annual Minimum Temperature':
        j = st.empty()
        k = st.empty()
        l = st.empty()

        with j:
            col1,col2 = st.columns(2)
            with col1:
                st.markdown('**Select the Latitude and Longitude**.')
                option_annual_min_temp = st.selectbox("", pd.DataFrame(lat_long_list),key = 8)

        Annual_temp_min = result.copy()
        df_min = annual_min_plot(Annual_temp_min,option_annual_min_temp,lat_long_list)
        fig_min = min_temp_plot(df_min,option_annual_min_temp)

        with k:
            st.plotly_chart(fig_min,use_container_width = True)

        #For maps
        lat_min  = float(option_annual_min_temp.split(',')[0])
        long_min = float(option_annual_min_temp.split(',')[1])

        with j:
            with col2:
                m_min = map_creation(lat_min,long_min,0,0)
                last_click = m_min['last_clicked']
                if last_click is not None:
                    clicked_lat = last_click['lat']
                    clicked_long = last_click['lng']
                    st.markdown("**Last Clicked Latitude Longitude point is:**")
                    st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                    nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                    st.write("**Nearest Latitude and Longitude is:**",nn)

                else:
                    st.markdown("**Click on the map to fetch the Latitude and Longitude**")
                    st.markdown("   ")
                    st.markdown("   ")
        with l:
            col100,col200,col300 = st.columns(3)
            with col200:
                st.download_button("Download Data",data = convert_df(df_min),
                                    file_name='Annual_minimum_temperature.csv',
                                    mime='text/csv',)

        with st.container():
            if nn!=0:
                nn_min_temp_df = annual_min_plot(Annual_temp_min,nn,lat_long_list)
                fig_min_nn = min_temp_plot(nn_min_temp_df,nn)
                with k:
                    st.plotly_chart(fig_min_nn, use_container_width = True)
                with l:
                    col11,col22,col33 = st.columns(3)
                    with col22:
                        st.download_button("Download Data",data = convert_df(nn_min_temp_df),
                                        file_name='Annual_minimum_temperature_nn.csv',
                                        mime='text/csv',)


    elif data_type == 'Annual Average Temperature':
        m = st.empty()
        n = st.empty()
        o = st.empty()
        annual_avg_df = result.copy()
        with m:
            col1,col2 = st.columns(2)
            with col1:
                st.markdown('**Select the Latitude and Longitude**')
                annual_avg_option = st.selectbox("",pd.DataFrame(lat_long_list),key = 9)
                annual_temp = annual_avg_plot(annual_avg_df,annual_avg_option,lat_long_list)
        with n:
            fig_avg = avg_temp_plot(annual_temp,annual_avg_option)
            st.plotly_chart(fig_avg,use_container_width = True)
        with o:
            col11,col22,col33 = st.columns(3)
            with col22:
                st.download_button("Download Data",
                               data = convert_df(annual_temp),
                               file_name='Annual_average_temperature.csv',
                               mime='text/csv',)
    #For maps
        lat_avg  = float(annual_avg_option.split(',')[0])
        long_avg = float(annual_avg_option.split(',')[1])
        with m:
            with col2:
                m_avg = map_creation(lat_avg,long_avg,0,0)
                last_click = m_avg['last_clicked']
                if last_click is not None:
                    clicked_lat = last_click['lat']
                    clicked_long = last_click['lng']
                    st.markdown("**Last Clicked Latitude Longitude point is:**")
                    st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))
                    nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                    st.write("**Nearest Latitude and Longitude is:**",nn)

                else:
                    st.markdown("**Click on the map to fetch the Latitude and Longitude**")

        with st.container():
            if nn!=0:
                nn_avg_temp_df = annual_avg_plot(annual_avg_df,nn,lat_long_list)
                fig_avg_nn = avg_temp_plot(nn_avg_temp_df,nn)
                with n:
                    st.plotly_chart(fig_avg_nn, use_container_width = True)
                with o:
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
                m_max_min_avg = map_creation(lat_avg_3,long_avg_3,0,0)

                last_click = m_max_min_avg['last_clicked']
                if last_click is not None:
                    clicked_lat = last_click['lat']
                    clicked_long = last_click['lng']
                    st.markdown("**Last Clicked Latitude Longitude point is:**")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.write("{:0.2f},{:0.2f}".format(clicked_lat,clicked_long))

                    nn = search_func(clicked_lat,clicked_long,lat_long_list,result)
                    st.write("**Nearest Latitude and Longitude is:**",nn)

                else:
                    st.markdown("**Click on the map to fetch the Latitude and Longitude**")

            col1,col2,col3 = st.columns(3)
            with col1:
                df1 = annual_max_plot(df,option_lat_long,lat_long_list)
                fig_2 = max_temp_plot(df1,option_lat_long)
                st.plotly_chart(fig_2, use_container_width=True)
                st.download_button("Download Data",
                                data = convert_df(df1),
                                file_name='Annual_maximum_temperature.csv',
                                mime='text/csv',)

                with st.container():
                    if nn!=0:
                        df_annual_max_2 = annual_max_plot(df,nn,lat_long_list)
                        fig_annual_max_nn_2 = max_temp_plot(df_annual_max_2,nn)
                        st.plotly_chart(fig_annual_max_nn_2, use_container_width=True)
                        st.download_button("Download Data",
                                        data = convert_df(df_annual_max_2),
                                        file_name='Annual_maximum_temperature_nn.csv',
                                        mime='text/csv',)

            with col2:
                with st.container():
                    df2 = annual_min_plot(df,option_lat_long,lat_long_list)
                    fig_3 = min_temp_plot(df2,option_lat_long)
                    st.plotly_chart(fig_3,use_container_width = True)
                    st.download_button("Download Data",
                                    data = convert_df(df2),
                                    file_name='Annual_minimum_temperature.csv',
                                    mime='text/csv',)
                with st.container():
                    if nn!=0:
                        df_annual_min_2 = annual_min_plot(df,nn,lat_long_list)
                        fig_annual_min_nn_2 = min_temp_plot(df_annual_min_2,nn)
                        st.plotly_chart(fig_annual_min_nn_2, use_container_width=True)
                        st.download_button("Download Data",
                                        data = convert_df(df_annual_min_2),
                                        file_name='Annual_minimum_temperature_nn.csv',
                                        mime='text/csv',)
            with col3:
                with st.container():
                    annual_average = annual_avg_plot(df,option_lat_long,lat_long_list)
                    fig_4 = avg_temp_plot(annual_average,option_lat_long)
                    st.plotly_chart(fig_4,use_container_width = True)

                    st.download_button("Download Data",
                                    data = convert_df(annual_average),
                                    file_name='Annual_average_temperature.csv',
                                    mime='text/csv',)

                with st.container():
                    if nn!=0:
                        df_annual_avg_nn_2 = annual_avg_plot(df,nn,lat_long_list)
                        fig_nn_4 = avg_temp_plot(df_annual_avg_nn_2,nn)
                        st.plotly_chart(fig_nn_4,use_container_width=True)
                        st.download_button("Download Data",
                                        data = convert_df(df_annual_avg_nn_2),
                                        file_name='Annual_average_temperature_nn.csv',
                                        mime='text/csv',)

if __name__ == 'main':
    run()
