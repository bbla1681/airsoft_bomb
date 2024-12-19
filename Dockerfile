# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application requirements file to the working directory
COPY requirements.txt /app/

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . /app

# Expose the port that the Flask app runs on
EXPOSE 8080

# Set environment variables for Google Cloud Run
ENV PORT=8080

# Command to run the Flask application
CMD ["python", "flask_control.py"]
