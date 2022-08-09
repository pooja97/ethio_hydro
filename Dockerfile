FROM python:3.8

WORKDIR /ethio_hydro_main/ethio_hydro

# Upgrade pip and install requirements

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Expose port you want your app on
EXPOSE 8501

# Copy app code and set working directory
COPY app.py app.py
COPY references references
COPY stlib stlib
COPY precipitation_function.py  precipitation_function.py
COPY temperature_functions.py   temperature_functions.py
COPY .streamlit .streamlit
COPY historicalData historicalData



# Run
RUN pip install streamlit
ENTRYPOINT ["streamlit", "run", "app.py"]
