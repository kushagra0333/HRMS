from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView

# RegisterView handles the user registration logic.
# It uses generics.CreateAPIView, which comes with pre-built logic for handling POST requests to create resources.
class RegisterView(generics.CreateAPIView):
    # The queryset determines the data scope this view works with (all users).
    queryset = User.objects.all()
    
    # permission_classes determines who can access this view.
    # AllowAny means even unauthenticated users (guests) can register.
    permission_classes = (permissions.AllowAny,)
    
    # serializer_class tells the view which Serializer to use to validate input and save data.
    serializer_class = RegisterSerializer

# EmployeeViewSet handles CRUD operations (Create, Retrieve, Update, Delete) for Employees.
# ModelViewSet automatically provides list, create, retrieve, update, and destroy actions.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id'

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
