from django.contrib import admin
from manyToMany.models import Student, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "get_courses_count",
        "get_courses_list",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at", "updated_at")

    def get_courses_count(self, obj):
        """Display the number of courses this student is enrolled in"""
        return obj.courses.count()

    get_courses_count.short_description = "Courses Count"

    def get_courses_list(self, obj):
        """Display list of course names"""
        courses = obj.courses.all()[:5]
        names = ", ".join([course.name for course in courses])
        if obj.courses.count() > 5:
            names += f" ... (+{obj.courses.count() - 5} more)"
        return names if names else "No courses"

    get_courses_list.short_description = "Courses"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_students_count",
        "get_students_list",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "students__name")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("students",)  # Better UI for selecting students

    def get_students_count(self, obj):
        """Display the number of students enrolled in this course"""
        return obj.students.count()

    get_students_count.short_description = "Students Count"

    def get_students_list(self, obj):
        """Display list of student names"""
        students = obj.students.all()[:5]
        names = ", ".join([student.name for student in students])
        if obj.students.count() > 5:
            names += f" ... (+{obj.students.count() - 5} more)"
        return names if names else "No students"

    get_students_list.short_description = "Students"
