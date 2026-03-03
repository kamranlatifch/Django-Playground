from django.db import models


class Student(models.Model):
    """
    Basic Student Information
    This is the main model - each student has basic info here
    """

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll_no = models.IntegerField(unique=True)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            # Composite: order_by('-created_at', 'roll_no') or filter + sort by created_at
            models.Index(fields=["-created_at", "roll_no"], name="student_created_roll_idx"),
        ]

    def __str__(self):
        return f"{self.name} (Roll: {self.roll_no})"


class StudentProfile(models.Model):
    """
    Detailed Student Profile
    ONE-TO-ONE RELATIONSHIP: Each Student has exactly ONE StudentProfile

    This model extends Student with additional information that:
    - Not all students might have (optional)
    - Is more detailed/private
    - Can be added later without changing the Student model
    """

    # ONE-TO-ONE RELATIONSHIP: One Student -> One StudentProfile
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,  # If student is deleted, profile is deleted too
        related_name="profile",  # Access profile via: student.profile
    )

    # Additional profile information
    bio = models.TextField(blank=True, help_text="Student's biography")
    profile_picture_url = models.URLField(
        blank=True, help_text="Link to profile picture"
    )
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    hobbies = models.TextField(blank=True, help_text="Student's hobbies and interests")
    achievements = models.TextField(blank=True, help_text="Awards, achievements, etc.")
    blood_group = models.CharField(max_length=5, blank=True)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.student.name}"
