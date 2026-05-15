from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, MeView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]
