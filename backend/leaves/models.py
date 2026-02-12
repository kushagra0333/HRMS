# We use djongo.models instead of django.db.models because we are likely using some MongoDB specific fields
# like ObjectIdField, though here we see standard fields too.
# Djongo allows using Django ORM with MongoDB.
from djongo import models
from employees.models import Employee

class Leave(models.Model):
    # Explicitly defining the primary key as an ObjectIdField.
    # MongoDB uses 12-byte BSON ObjectIds as primary keys.
    _id = models.ObjectIdField()
    
    # Choices for the status field. This limits the valid values to these three options.
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # ForeignKey links the Leave request to a specific Employee.
    # on_delete=models.CASCADE: If the Employee is deleted, all their leave requests are deleted too.
    # related_name='leaves': Allows us to access leaves from an employee object (e.g., employee.leaves.all()).
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    
    # The start and end dates of the leave period.
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Text field for the employee to explain why they are taking leave.
    reason = models.TextField()
    
    # Status of the request. Defaults to 'Pending' when created.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    # Automatically records when the leave request was made.
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation: "John Doe - Pending"
        return f"{self.employee.name} - {self.status}"
