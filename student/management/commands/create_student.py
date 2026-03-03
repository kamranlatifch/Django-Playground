"""
Management command with required/optional arguments.
Run with: python manage.py create_student "Alice" 20 101 alice@example.com "1234567890" "123 Main St"
Optional: python manage.py create_student "Bob" 21 102 bob@example.com "0987654321" "456 Oak Ave" --dry-run
"""
from django.core.management.base import BaseCommand

from student.models import Student


class Command(BaseCommand):
    help = "Creates a new Student (or dry-run to validate without saving)"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Student full name")
        parser.add_argument("age", type=int, help="Student age")
        parser.add_argument("roll_no", type=int, help="Unique roll number")
        parser.add_argument("email", type=str, help="Email address")
        parser.add_argument("phone", type=str, help="Phone number")
        parser.add_argument("address", type=str, help="Address")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and print data without saving to database",
        )

    def handle(self, *args, **options):
        name = options["name"]
        age = options["age"]
        roll_no = options["roll_no"]
        email = options["email"]
        phone = options["phone"]
        address = options["address"]
        dry_run = options["dry_run"]

        if Student.objects.filter(roll_no=roll_no).exists():
            self.stdout.write(self.style.ERROR(f"Roll number {roll_no} already exists."))
            return
        if Student.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"Email {email} already exists."))
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY RUN] Would create: {name}, age {age}, roll {roll_no}, {email}"
                )
            )
            return

        student = Student.objects.create(
            name=name,
            age=age,
            roll_no=roll_no,
            email=email,
            phone=phone,
            address=address,
        )
        self.stdout.write(self.style.SUCCESS(f"Created student: {student}"))
