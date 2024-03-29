# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 (the default port for Streamlit)
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["streamlit", "run", "sketch_app.py"]
