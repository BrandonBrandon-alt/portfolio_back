#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    # Cargar la variable de entorno DATABASE_URL si está en .env
    os.environ.setdefault('DATABASE_URL', config('DATABASE_URL', default=''))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portafolio.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
