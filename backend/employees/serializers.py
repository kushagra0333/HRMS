from rest_framework import serializers
from .models import Employee
from django.contrib.auth.models import User

# Serializers convert complex data (like model instances) into native Python data types 
# that can then be easily rendered into JSON, XML or other content types.
# They also handle deserialization (validating input data before saving).

# Serializer for the standard Django User model.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Only expose these specific fields to the API.
        fields = ('id', 'username', 'email')

# Serializer for handling registration requests.
# It validates the username, password, email, etc.
class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True means these fields are accepted in input but never sent back in the output.
    password = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'department')

    # The create method defines what happens when we save valid data.
    def create(self, validated_data):
        # Create the standard User object first.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'] 
        )
        
        # After creating the User, we immediately create the linked Employee profile.
        # This ensures every User has an Employee record.
        Employee.objects.create(
            user=user,
            # For simplicity, we use the username (converted to uppercase) as the Employee ID.
            # In a real system, you might want a specific ID generation logic.
            employee_id=validated_data.get('username').upper(), 
            name=validated_data['first_name'],
            email=validated_data['email'],
            department=validated_data['department']
        )
        return user

# Serializer for the Employee model itself.
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # '__all__' means we expose every field in the model to the API.
        fields = '__all__'
