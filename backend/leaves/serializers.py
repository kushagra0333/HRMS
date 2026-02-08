from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    employee_name = serializers.ReadOnlyField(source='employee.name')
    employee_id = serializers.ReadOnlyField(source='employee.employee_id')

    def get_id(self, obj):
        return str(obj.pk)

    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ('employee', 'status') 
