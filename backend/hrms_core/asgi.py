"""
ASGI config for hrms_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default settings module for the 'asgi' application.
# ASGI is the asynchronous version of WSGI, allowing for things like WebSockets.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_core.settings')

# Get the ASGI application.
# This 'application' object is what an ASGI server (like Uvicorn or Daphne) talks to.
application = get_asgi_application()
