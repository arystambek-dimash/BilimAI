#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bilim_ai.settings')
    media_dir = "media/"
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    images_dir = os.path.join(media_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    videos_dir = os.path.join(media_dir, "videos")
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

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
