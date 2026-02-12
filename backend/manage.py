#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the entry point for running commands like:
- python manage.py runserver (starts the dev server)
- python manage.py migrate (updates database schema)
- python manage.py startapp (creates a new app)
"""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # Set the default Django settings module.
    # This tells Django where to find the configuration (settings.py).
    # 'hrms_core.settings' means the file settings.py insde the hrms_core folder.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_core.settings')
    
    try:
        # Import the function that actually executes the commands.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed or the virtual environment is not activated, this error will be raised.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # valid command line arguments (sys.argv) are passed to the execute function.
    # e.g., ['manage.py', 'runserver']
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # This block ensures that main() runs only when the script is executed directly,
    # not when it is imported as a module.
    main()
