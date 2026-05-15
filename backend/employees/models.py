from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# The Employee model represents the employee entity in our system.
# It stores information about each staff member.
class Employee(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    # OneToOneField creates a link between this Employee record and a standard Django User record.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

@receiver(post_save, sender=User)
def create_user_employee(sender, instance, created, **kwargs):
    if created:
        # Check if user is superuser to assign admin role
        role = 'admin' if instance.is_superuser else 'employee'
        Employee.objects.update_or_create(
            user=instance,
            defaults={
                'employee_id': f"EMP{instance.id:04d}",
                'name': instance.username,
                'email': instance.email,
                'role': role,
                'department': 'General'
            }
        )
