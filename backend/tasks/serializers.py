from rest_framework import serializers
from .models import Project, Task
from employees.models import Employee

class EmployeeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'employee_id', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.name')
    assigned_by_name = serializers.ReadOnlyField(source='assigned_by.name')
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Employee.objects.all()
    )
    member_details = EmployeeSimpleSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'deadline', 'status', 'members', 'member_details', 'tasks', 'created_at', 'updated_at')
