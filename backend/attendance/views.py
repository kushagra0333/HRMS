from rest_framework import viewsets, permissions, serializers
from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee

# Exceptions we might need to catch when saving to stats
from django.db import IntegrityError, DatabaseError
from pymongo.errors import BulkWriteError

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom QuerySet:
    # Admins see all records.
    # Employees see only their own records.
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Attendance.objects.all().order_by('-date')
        try:
            return Attendance.objects.filter(employee=user.employee).order_by('-date')
        except Employee.DoesNotExist:
            return Attendance.objects.none()

    # Custom Creation Logic:
    # When creating an attendance record, we automatically link it to the current user's employee profile.
    def perform_create(self, serializer):
        try:
           serializer.save(employee=self.request.user.employee)
        except Employee.DoesNotExist:
            # Prevent users without employee profiles from marking attendance.
            raise serializers.ValidationError("User is not linked to an Employee profile.")
        except (IntegrityError, BulkWriteError, DatabaseError):
            # This catches the 'unique_together' constraint violation from the model
            # (i.e., if they already marked attendance for today).
            raise serializers.ValidationError("Attendance already marked for this date.")
