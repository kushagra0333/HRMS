from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

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


def generate_employee_id(user):
    username = (user.username or "").strip().upper()
    normalized_username = re.sub(r"[^A-Z0-9]+", "_", username).strip("_")
    if normalized_username:
        return normalized_username

    return f"EMP_{str(user.pk).replace('-', '').upper()[-8:]}"

@receiver(post_save, sender=User)
def create_user_employee(sender, instance, created, **kwargs):
    if created:
        # Check if user is superuser to assign admin role
        role = 'admin' if instance.is_superuser else 'employee'
        Employee.objects.update_or_create(
            user=instance,
            defaults={
                'employee_id': generate_employee_id(instance),
                'name': instance.username,
                'email': instance.email,
                'role': role,
                'department': 'General'
            }
        )
