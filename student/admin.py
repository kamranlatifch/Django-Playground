from django.contrib import admin
from student.models import Student, StudentProfile


# Inline Admin for StudentProfile
# This allows editing the profile directly from the Student admin page
class StudentProfileInline(admin.StackedInline):
    """
    Inline admin for StudentProfile
    This shows the profile fields directly on the Student edit page
    """

    model = StudentProfile
    can_delete = False  # Can't delete profile separately
    verbose_name_plural = "Student Profile"
    fieldsets = (
        (
            "Biography",
            {"fields": ("bio", "profile_picture_url", "hobbies", "achievements")},
        ),
        (
            "Emergency Contact",
            {"fields": ("emergency_contact", "emergency_phone", "blood_group")},
        ),
        ("Parent Information", {"fields": ("parent_name", "parent_email")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin for Student model
    Includes inline for StudentProfile (one-to-one relationship)
    """

    list_display = (
        "name",
        "roll_no",
        "email",
        "age",
        "has_profile",  # Custom method to show if profile exists
        "created_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email", "phone", "address", "roll_no")
    readonly_fields = ("created_at", "updated_at")

    # Add the inline - this is the KEY for one-to-one relationships!
    inlines = [StudentProfileInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "age", "roll_no", "email", "phone", "address")},
        ),
        ("Statistics", {"fields": ("created_at", "updated_at")}),
    )

    def has_profile(self, obj):
        """Check if student has a profile (one-to-one relationship check)"""
        try:
            return bool(obj.profile)  # Access via related_name='profile'
        except StudentProfile.DoesNotExist:
            return False

    has_profile.boolean = True
    has_profile.short_description = "Has Profile"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    Standalone admin for StudentProfile
    You can also edit profiles separately if needed
    """

    list_display = ("student", "emergency_contact", "parent_name", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = (
        "student__name",
        "student__email",
        "emergency_contact",
        "parent_name",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Student", {"fields": ("student",)}),
        (
            "Biography",
            {"fields": ("bio", "profile_picture_url", "hobbies", "achievements")},
        ),
        (
            "Emergency Contact",
            {"fields": ("emergency_contact", "emergency_phone", "blood_group")},
        ),
        ("Parent Information", {"fields": ("parent_name", "parent_email")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
