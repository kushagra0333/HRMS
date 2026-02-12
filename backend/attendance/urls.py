from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

# DefaultRouter creates standard REST API routes for the viewset.
router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    # Include the router's URLs.
    # This provides endpoints like:
    # GET /api/attendance/ (List)
    # POST /api/attendance/ (Create)
    path('', include(router.urls)),
]
