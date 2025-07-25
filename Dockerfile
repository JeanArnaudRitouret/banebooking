# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
# COPY pyproject.toml poetry.lock README.md ./

# Install Poetry
RUN pip install poetry

# 1) Copy just your Poetry config first
COPY pyproject.toml poetry.lock README.md ./

# 2) Turn off virtualenv creation
RUN poetry config virtualenvs.create false

# Copy the entire project
COPY banebooking/ banebooking/
COPY matchi/ matchi/
COPY manage.py manage.py

# 3) Install dependencies
RUN poetry install --no-interaction --no-ansi


# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["sh", "-c", "python manage.py migrate && gunicorn --timeout 120 --workers 1 --bind 0.0.0.0:8080 matchi.wsgi:application"]