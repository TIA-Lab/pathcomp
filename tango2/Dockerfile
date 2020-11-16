# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /app 
#ADD . /app
COPY requirements.txt /app

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
