# Use an official Python runtime as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port on which your Django app will run
EXPOSE 8000

# Run the Django app using Gunicorn
CMD ["gunicorn", "photobooth.wsgi", "--bind", "0.0.0.0:8000"]
