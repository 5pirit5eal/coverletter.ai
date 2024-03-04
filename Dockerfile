# Use the official Python 3.11 image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY app .

# Expose the port that the Streamlit app will run on
EXPOSE 8501
ENV HOST 0.0.0.0

# Set the command to run the Streamlit app when the container starts
CMD [ "sh", "-c", "streamlit run --server.port ${PORT} --server.address ${HOST} /app/main.py" ]