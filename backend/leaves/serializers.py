from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    # SerializerMethodField allows us to define a custom field that is calculated by a method.
    # Here, we mapped 'id' to get_id method.
    id = serializers.SerializerMethodField()
    
    # ReadOnlyField gets data from the related model (Employee) by dot notation.
    # This prevents the client from trying to change the employee name/id via this endpoint.
    employee_name = serializers.ReadOnlyField(source='employee.name')
    employee_id = serializers.ReadOnlyField(source='employee.employee_id')

    # This method returns the string representation of the object's primary key.
    # This is often needed with MongoDB ObjectIds to ensure they are returned as strings, not objects.
    def get_id(self, obj):
        return str(obj.pk)

    class Meta:
        model = Leave
        fields = '__all__' # Expose all fields
        # These fields cannot be modified by the user in a request (like POST or PUT).
        # We don't want users arbitrarily changing the status (only admins should) or the employee link.
        read_only_fields = ('employee', 'status') 
