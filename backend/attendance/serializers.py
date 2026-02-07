from rest_framework import serializers
from .models import Attendance
from employees.models import Employee

class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        slug_field='employee_id',
        queryset=Employee.objects.all()
    )

    class Meta:
        model = Attendance
        fields = '__all__'
