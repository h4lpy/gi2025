# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create flag.txt file with the desired text
RUN echo "GRIDIRON{easy_command_injection_a3c516e6e}" > /flag.txt

# Expose port 8080 to the outside world
EXPOSE 8080

# Define environment variable
ENV FLASK_APP main.py

# Run main.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
