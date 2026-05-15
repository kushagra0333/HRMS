
# Importing the admin module to enable the admin interface.
from django.contrib import admin

# path: used for standard URL routing.
# include: used to reference other URL configurations (from apps).
# re_path: used for regex-based URL routing (for complex patterns).
from django.urls import path, include, re_path

# Import views from the local directory (hrms_core/views.py)
from . import views
from django.views.generic import RedirectView

# Import JWT views for handling token generation and refreshing.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Route for the built-in Django admin interface.
    # Accessing /admin/ opens the dashboard to manage models.
    path('admin/', admin.site.urls),
    
    # Root static files for React
    path('manifest.json', RedirectView.as_view(url='/static/manifest.json', permanent=True)),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('logo192.png', RedirectView.as_view(url='/static/logo192.png', permanent=True)),
    path('logo512.png', RedirectView.as_view(url='/static/logo512.png', permanent=True)),

    # API routes. 'include' delegates the request to the specific app's urls.py.
    # Any URL starting with 'api/' and matching what's in 'employees.urls' goes there.
    path('api/', include('employees.urls')),
    path('api/', include('attendance.urls')),
    path('api/', include('leaves.urls')),
    path('api/', include('tasks.urls')),
    
    # Example route comment: needs cleanup or consolidation into employees.urls
    path('api/auth/register/', include('employees.auth_urls')), 

    # Key authentication endpoints:
    path('api/deploy-info/', views.deploy_info, name='deploy_info'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Catch-all route for serving the React Frontend.
    # We use a regex that avoids catching URLs that look like file requests (contain a dot)
    # or start with api/ or admin/
    re_path(r'^(?!api|admin|static|.*?\..*?).*$', views.index, name='index'),
    
    # Alternatively, just serve the index for everything else, but ensure WhiteNoise
    # has a chance to serve the static files first.
    re_path(r'^.*$', views.index, name='index'),
]
