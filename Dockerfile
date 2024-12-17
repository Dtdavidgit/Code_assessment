# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas matplotlib 

# Command to run the Python script
ENTRYPOINT ["python", "taxonomic_analysis.py"]
CMD ["-h"]