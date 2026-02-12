from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

# DRF Routers automatically generate URL patterns for ViewSets.
# Since EmployeeViewSet is a ModelViewSet, it supports GET (list), POST (create), 
# GET (retrieve), PUT (update), DELETE (destroy).
router = DefaultRouter()

# Register the ViewSet with the router.
# This creates URLs like:
# /employees/ -> List all employees or create new one
# /employees/{employee_id}/ -> Get, update, or delete a specific employee
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    # Include the auto-generated router URLs.
    path('', include(router.urls)),
]
