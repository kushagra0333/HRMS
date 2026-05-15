from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from employees.models import Employee

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            if employee.role == 'admin':
                return Project.objects.all()
            return Project.objects.filter(members=employee)
        except AttributeError:
            return Project.objects.none()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
            if employee.role == 'admin':
                return Task.objects.all()
            return Task.objects.filter(assigned_to=employee)
        except AttributeError:
            return Task.objects.none()

    def perform_create(self, serializer):
        try:
            employee = self.request.user.employee
            serializer.save(assigned_by=employee)
        except AttributeError:
            serializer.save()

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            task.status = new_status
            task.save()
            return Response({'status': 'status updated'})
        return Response({'error': 'status not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_checklist(self, request, pk=None):
        task = self.get_object()
        checklist = request.data.get('checklist')
        if checklist is not None:
            task.checklist = checklist
            task.save()
            return Response({'status': 'checklist updated'})
        return Response({'error': 'checklist not provided'}, status=status.HTTP_400_BAD_REQUEST)
