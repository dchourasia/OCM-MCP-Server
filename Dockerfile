# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code and settings into the container
COPY src/ocm_server.py .
COPY src/settings.py .
# Note: .env file with secrets should be mounted, not copied.
# We can copy the .env.example for reference or if default fallbacks are desired.
# COPY config/.env.example .

# Make port 8000 available to the world outside this container
# This is for the streamable-http transport
EXPOSE 8000

# Define environment variable for Python to output unbuffered logs
ENV PYTHONUNBUFFERED 1

# Run ocm_server.py when the container launches
# Defaulting to streamable-http transport on port 8000, listening on all interfaces (0.0.0.0)
CMD ["fastmcp", "run", "ocm_server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]