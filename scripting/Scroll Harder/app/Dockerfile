# Dockerfile

# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the required files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir Flask qrcode[pil]

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
