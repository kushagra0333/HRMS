from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    # Enum-like choices for attendance status.
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    # Link to the Employee model.
    # on_delete=models.CASCADE: If employee is deleted, their attendance records are gone too.
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    
    # The date of attendance.
    date = models.DateField()
    
    # Status: Preset vs Absent.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        # unique_together ensures that an employee cannot have two attendance records for the same date.
        # This prevents duplicate entries.
        unique_together = ('employee', 'date')
        
        # Default ordering: newest dates first.
        ordering = ['-date']

    def __str__(self):
        # String representation: "John Doe - 2023-10-27 - Present"
        return f"{self.employee.name} - {self.date} - {self.status}"
