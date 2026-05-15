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
        try:
            employee = user.employee
            if employee.role == 'admin':
                return Attendance.objects.all().order_by('-date')
            return Attendance.objects.filter(employee=employee).order_by('-date')
        except AttributeError:
            return Attendance.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = user.employee
            if employee.role == 'admin' and 'employee' in self.request.data:
                # Admin can specify employee ID
                serializer.save()
            else:
                # Others (or admin not specifying) default to self
                serializer.save(employee=employee)
        except AttributeError:
            raise serializers.ValidationError("User is not linked to an Employee profile.")
        except (IntegrityError, BulkWriteError, DatabaseError):
            raise serializers.ValidationError("Attendance already marked for this date.")
