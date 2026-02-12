from rest_framework import serializers
from .models import Attendance
from employees.models import Employee

class AttendanceSerializer(serializers.ModelSerializer):
    # SlugRelatedField allows us to represent the 'employee' relationship
    # using the 'employee_id' field (string) instead of the database ID (integer/ObjectId).
    # When reading, it shows the employee_id. When writing, it expects an employee_id to find the object.
    employee = serializers.SlugRelatedField(
        slug_field='employee_id',
        queryset=Employee.objects.all()
    )

    class Meta:
        model = Attendance
        # Expose all fields including the computed/related ones.
        fields = '__all__'
