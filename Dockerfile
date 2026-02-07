# Build Stage for Frontend
FROM node:20-alpine as frontend_build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final Stage for Backend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy frontend build artifacts to backend destination
# Destination matches BASE_DIR / 'react_build' in settings.py
COPY --from=frontend_build /app/frontend/build /app/react_build

# Run patch script if needed (from original backend Dockerfile)
RUN python patch_djongo.py

# Collect static files
# This gathers admin static files AND react static files (via STATICFILES_DIRS) into STATIC_ROOT
RUN python manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=hrms_core.settings

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn hrms_core.wsgi:application --bind 0.0.0.0:8000"]
