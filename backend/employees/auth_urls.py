from django.urls import path
from .views import RegisterView

# specific URL patterns for authentication-related actions handled by this app.
urlpatterns = [
    # Route for registration.
    # RegisterView.as_view() converts the class-based view into a function Django can use.
    path('', RegisterView.as_view(), name='register'),
]
