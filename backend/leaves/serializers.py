from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    employee_id = serializers.ReadOnlyField(source='employee.employee_id')

    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ('employee', 'status') 
