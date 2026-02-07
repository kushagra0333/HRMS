from rest_framework import serializers
from .models import Employee
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'department')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'] # Using first_name as Name for simplicity or add name field?
        )
        # Employee model has 'name' field. Map first_name to it?
        # Or just accept 'name' in input and save it to Employee.
        
        Employee.objects.create(
            user=user,
            employee_id=validated_data.get('username').upper(), # Use username as ID for simplicity? Or generate one?
            # User wants to login.
            name=validated_data['first_name'],
            email=validated_data['email'],
            department=validated_data['department']
        )
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
