"""
Minimal management command example.
Run with: python manage.py greet
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints a simple greeting (minimal management command example)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Hello from Django! 👋"))
