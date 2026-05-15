from django.db import models
from employees.models import Employee

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(Employee, related_name='projects')
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    checklist = models.JSONField(default=list) # List of {text: string, completed: boolean}
    completion_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
