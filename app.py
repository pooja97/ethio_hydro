#standard imports
import pandas as pd
import streamlit as st
from PIL import Image



# Setting the Page Layout as wide

st.set_page_config(
    page_title="AI GERD Dashboard",
    layout="wide")

# # Creating Container for Logo and Title
with st.container():
    col1,col2 = st.columns(2)
    #Code for adding Logo
    with col1:
        image = Image.open('references/image.png')
        st.image(image)
    #Code for Title
    with col2:
        col2.markdown("<h1 style='text-align:centre; color: black;'>ETHIO HYDRO & CLIMATE HUB</h1>", unsafe_allow_html=True)

message = """
            __Select an application from the list below__
            """

from stlib import precipitation
from stlib import temperature


with st.sidebar:
    st.markdown(message)
    page = st.selectbox(' ',['Temperature',"Precipitation"])


if page == 'Temperature':
    temperature.run()

elif page == 'Precipitation':
    precipitation.run()
