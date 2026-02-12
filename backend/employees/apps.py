from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    # This class configures the 'employees' app.
    # It tells Django the name of the app and can be used for advanced initialization
    # (like setting up signals when the app is ready).
    name = 'employees'
