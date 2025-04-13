#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc

    # Add both the project root and the apps directory to the Python path
    current_path = Path(__file__).parent
    sys.path.append(str(current_path))
    sys.path.append(str(current_path / 'apps'))
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
