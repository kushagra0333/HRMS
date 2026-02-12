"""
WSGI config for hrms_core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'wsgi' application.
# This ensures that when the server starts, it knows which settings to load.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_core.settings')

# specialized WSGI application serves the Django app.
# This 'application' object is what the web server (like Gunicorn) talks to.
application = get_wsgi_application()
