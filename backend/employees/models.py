from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# The Employee model represents the employee entity in our system.
# It stores information about each staff member.
class Employee(models.Model):
    # OneToOneField creates a link between this Employee record and a standard Django User record.
    # on_delete=models.CASCADE means if the User is deleted, the Employee profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # A unique identifier for the employee (e.g., "EMP001").
    employee_id = models.CharField(max_length=20, unique=True)
    
    # Simple character fields for name and department.
    name = models.CharField(max_length=100)
    
    # Email field ensures valid email format and uniqueness.
    email = models.EmailField(unique=True)
    
    department = models.CharField(max_length=100)
    
    # Automatically records the date and time when the record was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the object. This is what you see in the admin panel.
    def __str__(self):
        return f"{self.name} ({self.employee_id})"

# Signals allow certain "senders" to notify a set of "receivers" that some action has taken place.
# Here, we listen for the 'post_save' signal sent by the User model.
@receiver(post_save, sender=User)
def create_user_employee(sender, instance, created, **kwargs):
    # This function runs every time a User object is saved.
    if created:
        # If a new user was just created (created=True), we could auto-generate an Employee profile here.
        # Currently, it does pass (nothing), but this is a common pattern for automatically
        # creating related profiles.
        pass
