FROM python:3.9.12

# Expose port you want your app on
#EXPOSE 8501

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY app.py app.py

WORKDIR .

# Run
ENTRYPOINT ['streamlit','run']
CMD ["app.py"]
