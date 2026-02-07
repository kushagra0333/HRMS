FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run patch script
RUN python patch_djongo.py

# Collect static files
# RUN python manage.py collectstatic --noinput
# (Optional: If using WhiteNoise, run this. Or handle static files via Nginx/Volume)
# For now, let's keep it simple.

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=hrms_core.settings

# Expose port
EXPOSE 8000

# Run migrations and start server
# Using a shell script entrypoint is often safer for migrations, but we can chain commands
CMD ["sh", "-c", "python manage.py migrate && gunicorn hrms_core.wsgi:application --bind 0.0.0.0:8000"]
