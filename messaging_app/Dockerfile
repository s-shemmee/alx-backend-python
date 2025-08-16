<<<<<<< HEAD
# Dockerfile for Django Messaging App
FROM python:3.10
=======
# Use official Python image as base
FROM python:3.10-slim
>>>>>>> d0490bfd6050893ba6fe451657340bb3fed08906

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

<<<<<<< HEAD
# Install dependencies
=======
# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
>>>>>>> d0490bfd6050893ba6fe451657340bb3fed08906
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

<<<<<<< HEAD
# Expose port 8000
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
=======
# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver -p 8000 0.0.0.0:8000"]
>>>>>>> d0490bfd6050893ba6fe451657340bb3fed08906
