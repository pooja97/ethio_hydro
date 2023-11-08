# Time Series GeoSpatial Data Analysis | Streamlit and Docker

## Introduction

Data Analysis on Ethiopia's rain and temperature data collected from the [SWAT](https://swat.tamu.edu/data/) database using various tools and technologies, including Streamlit, python3, Docker, and plotly.js

## Technologies Used
Programming Language: 
    1. python3<br>

Tools and Data Visualization:<br>
    1. Docker <br>
    2. Streamlit <br>
    3. Folium<br>
    4. plotly.js<br>

Created a dashboard using Streamlit and python3 to analyze and monitor Ethiopia's rain and temperature time series data collected from the SWAT database. Cleaned and manipulated the data using geoPy to extract Ethiopia's data and implemented parallel processing using Swifter and Pandarallel. Added functionalities to display daily average temperature, monthly mean temperature, Annual Max, Min, and Average temperature, Daily precipitation, min, max, and average precipitation, and Cumulative and monthly average precipitation. 
Created Ethiopia's map and implemented a bi-directional communication using haversine distance to fetch the nearest location and display the fetched locations data using streamlit-folium, branca, and Numpy. Containerized the application using Docker. 

Deployed it on [HuggingFace](https://huggingface.co/spaces/poooja2012/ethio_hydro) 


