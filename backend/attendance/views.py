from rest_framework import viewsets, permissions, serializers
from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all().order_by('-date')
        try:
            return Attendance.objects.filter(employee=user.employee).order_by('-date')
        except Employee.DoesNotExist:
            return Attendance.objects.none()

    def perform_create(self, serializer):
        try:
           serializer.save(employee=self.request.user.employee)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("User is not linked to an Employee profile.")
