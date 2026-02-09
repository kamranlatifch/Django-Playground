from django.contrib import admin

from student.models import Student

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "roll_no",
        "email",
        "address",
        "created_at",
        "updated_at",
    )
    list_filter = ("name", "created_at", "updated_at")
    search_fields = ("name", "email", "phone", "address", "roll_no")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Content",
            {"fields": ("name", "age", "roll_no", "email", "phone", "address")},
        ),
        ("Statistics", {"fields": ("created_at", "updated_at")}),
    )
