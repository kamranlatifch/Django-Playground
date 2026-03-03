"""
Management command that uses the database (Student model).
Run with: python manage.py list_students
Optional: python manage.py list_students --count 5
"""
from django.core.management.base import BaseCommand

from student.models import Student


class Command(BaseCommand):
    help = "Lists students from the database (optionally limited by count)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=None,
            help="Maximum number of students to list (default: all)",
        )

    def handle(self, *args, **options):
        qs = Student.objects.all().order_by("roll_no")
        count = options.get("count")
        if count is not None:
            qs = qs[:count]

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No students in the database."))
            return

        self.stdout.write(self.style.SUCCESS(f"Students (showing up to {count or total}):"))
        for s in qs:
            self.stdout.write(f"  • {s.name} (Roll: {s.roll_no}, {s.email})")
