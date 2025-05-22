# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional for admin UI)
RUN python manage.py collectstatic --noinput

# Run app
CMD ["gunicorn", "lead_project.wsgi:application", "--bind", "0.0.0.0:8000"]
