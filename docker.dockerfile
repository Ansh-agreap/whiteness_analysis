# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Create uploads directory
RUN mkdir uploads

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies required by OpenCV and other libraries
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 6000

# Run your application
CMD ["python", "stage_app.py"]
######################### WORKING ###################################3
# # Use an official Python runtime as a parent image
# FROM python:3.10-slim

# # Set the working directory
# WORKDIR /stage_app

# # Copy the current directory contents into the container at /app, mount local volume to docker
# COPY . /stage_app 

# # Copy requirements.txt into the container
# COPY requirements.txt /stage_app/

# # Create the uploads directory
# RUN mkdir -p /stage_app/uploads

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir --timeout=500 -r requirements.txt


# # Install system dependencies required by OpenCV and other libraries
# RUN apt-get update && \
#     apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Make port 5000 available to the world outside this container (if applicable)
# EXPOSE 5000

# # Run your application
# CMD ["python", "stage_app.py"]


#############FAST API###########################################3
# FROM python:3.10-slim

# # Set the working directory
# WORKDIR /stage_app

# # Copy the current directory contents into the container
# COPY . /stage_app

# # Copy requirements.txt into the container
# COPY requirements.txt /stage_app/

# # Create the uploads directory
# RUN mkdir -p /stage_app/uploads

# # Install Python dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Install system dependencies required by OpenCV and other libraries
# RUN apt-get update && \
#     apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Expose the port on which the FastAPI app will run
# EXPOSE 6000

# # Command to run the FastAPI app
# CMD ["uvicorn", "stage_app:stage_app", "--host", "0.0.0.0", "--port", "6000", "--reload"]
