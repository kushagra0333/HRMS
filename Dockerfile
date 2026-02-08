# Stage 1: Build the React Frontend
FROM node:16 as build-stage
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup the Django Backend
FROM python:3.9
WORKDIR /app/backend

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy React build artifacts from Stage 1
# Ensure the destination matches where Django looks for static files/templates
COPY --from=build-stage /app/frontend/build ./react_build

# Run collectstatic to prepare files for WhiteNoise
RUN python manage.py collectstatic --no-input

# Gunicorn will start the app
# The bind address 0.0.0.0 is crucial for Docker
CMD ["gunicorn", "hrms_core.wsgi:application", "--bind", "0.0.0.0:10000"]
