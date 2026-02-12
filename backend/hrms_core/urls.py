"""
URL configuration for hrms_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

# Importing the admin module to enable the admin interface.
from django.contrib import admin

# path: used for standard URL routing.
# include: used to reference other URL configurations (from apps).
# re_path: used for regex-based URL routing (for complex patterns).
from django.urls import path, include, re_path

# Import views from the local directory (hrms_core/views.py)
from . import views

# Import JWT views for handling token generation and refreshing.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Route for the built-in Django admin interface.
    # Accessing /admin/ opens the dashboard to manage models.
    path('admin/', admin.site.urls),

    # API routes. 'include' delegates the request to the specific app's urls.py.
    # Any URL starting with 'api/' and matching what's in 'employees.urls' goes there.
    path('api/', include('employees.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('leaves.urls')),
    
    # Example route comment: needs cleanup or consolidation into employees.urls
    path('api/auth/register/', include('employees.auth_urls')), 

    # Key authentication endpoints:
    # Login endpoint: POST a username/password, get back an Access and Refresh token.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Refresh endpoint: POST a Refresh token, get back a new Access token.
    # This allows users to stay logged in without re-entering passwords constantly.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Catch-all route for serving the React Frontend.
    # re_path(r'^.*$') matches ANY URL that hasn't been matched above.
    # It sends them to views.index, which serves the React index.html.
    # This allows React Router to handle the frontend routing (Client-Side Routing).
    re_path(r'^.*$', views.index, name='index'),
]
