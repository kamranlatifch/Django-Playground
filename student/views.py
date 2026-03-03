from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, StudentProfile


def student_list(request):
    """Display list of all students"""
    students = Student.objects.all().order_by("-created_at")
    return render(request, "student/student_list.html", {"students": students})


def student_detail(request, id):
    """Display details of a single student"""
    student = get_object_or_404(Student, id=id)
    # Try to get profile if it exists
    try:
        profile = student.profile
    except StudentProfile.DoesNotExist:
        profile = None
    return render(
        request, "student/student_detail.html", {"student": student, "profile": profile}
    )


def student_create(request):
    """Create a new student"""
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        age = request.POST.get("age")
        roll_no = request.POST.get("roll_no")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Validate required fields
        if name and age and roll_no and email and phone and address:
            try:
                # Create student
                student = Student.objects.create(
                    name=name,
                    age=int(age),
                    roll_no=int(roll_no),
                    email=email,
                    phone=phone,
                    address=address,
                )
                messages.success(
                    request, f"Student {student.name} created successfully!"
                )
                return redirect("student_detail", id=student.id)
            except Exception as e:
                messages.error(request, f"Error creating student: {str(e)}")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "student/student_form.html", {"form_type": "Create"})


def student_update(request, id):
    """Update an existing student"""
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        age = request.POST.get("age")
        roll_no = request.POST.get("roll_no")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Validate required fields
        if name and age and roll_no and email and phone and address:
            try:
                # Update student
                student.name = name
                student.age = int(age)
                student.roll_no = int(roll_no)
                student.email = email
                student.phone = phone
                student.address = address
                student.save()
                messages.success(
                    request, f"Student {student.name} updated successfully!"
                )
                return redirect("student_detail", id=student.id)
            except Exception as e:
                messages.error(request, f"Error updating student: {str(e)}")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(
        request,
        "student/student_form.html",
        {"student": student, "form_type": "Update"},
    )


def student_delete(request, id):
    """Delete a student"""
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student_name = student.name
        student.delete()
        messages.success(request, f"Student {student_name} deleted successfully!")
        return redirect("student_list")

    return render(request, "student/student_confirm_delete.html", {"student": student})


# ============================================
# PROFILE VIEWS
# ============================================


def profile_list(request):
    """Display list of all profiles"""
    profiles = StudentProfile.objects.all().order_by("-created_at")
    return render(request, "student/profile_list.html", {"profiles": profiles})


def profile_detail(request, id):
    """Display details of a single profile"""
    profile = get_object_or_404(StudentProfile, id=id)
    return render(request, "student/profile_detail.html", {"profile": profile})


def profile_create(request):
    """Create a profile for a student"""
    if request.method == "POST":
        # Get form data
        student_id = request.POST.get("student")
        bio = request.POST.get("bio", "")
        profile_picture_url = request.POST.get("profile_picture_url", "")
        emergency_contact = request.POST.get("emergency_contact", "")
        emergency_phone = request.POST.get("emergency_phone", "")
        hobbies = request.POST.get("hobbies", "")
        achievements = request.POST.get("achievements", "")
        blood_group = request.POST.get("blood_group", "")
        parent_name = request.POST.get("parent_name", "")
        parent_email = request.POST.get("parent_email", "")

        if not student_id:
            messages.error(request, "Please select a student.")
        else:
            try:
                student = Student.objects.get(id=student_id)

                # Check if profile already exists
                if hasattr(student, "profile"):
                    messages.info(
                        request,
                        f"Profile for {student.name} already exists. You can update it instead.",
                    )
                    return redirect("profile_update", id=student.profile.id)

                # Create profile
                profile = StudentProfile.objects.create(
                    student=student,
                    bio=bio,
                    profile_picture_url=profile_picture_url,
                    emergency_contact=emergency_contact,
                    emergency_phone=emergency_phone,
                    hobbies=hobbies,
                    achievements=achievements,
                    blood_group=blood_group,
                    parent_name=parent_name,
                    parent_email=parent_email,
                )
                messages.success(
                    request, f"Profile for {student.name} created successfully!"
                )
                return redirect("profile_detail", id=profile.id)
            except Student.DoesNotExist:
                messages.error(request, "Selected student does not exist.")
            except Exception as e:
                messages.error(request, f"Error creating profile: {str(e)}")

    # Get all students without profiles
    students_without_profile = Student.objects.filter(profile__isnull=True)
    all_students = Student.objects.all()

    return render(
        request,
        "student/profile_form.html",
        {
            "students": all_students,
            "students_without_profile": students_without_profile,
            "form_type": "Create",
        },
    )


def profile_update(request, id):
    """Update an existing profile"""
    profile = get_object_or_404(StudentProfile, id=id)
    student = profile.student

    if request.method == "POST":
        # Get form data
        student_id = request.POST.get("student")
        bio = request.POST.get("bio", "")
        profile_picture_url = request.POST.get("profile_picture_url", "")
        emergency_contact = request.POST.get("emergency_contact", "")
        emergency_phone = request.POST.get("emergency_phone", "")
        hobbies = request.POST.get("hobbies", "")
        achievements = request.POST.get("achievements", "")
        blood_group = request.POST.get("blood_group", "")
        parent_name = request.POST.get("parent_name", "")
        parent_email = request.POST.get("parent_email", "")

        if not student_id:
            messages.error(request, "Please select a student.")
        else:
            try:
                new_student = Student.objects.get(id=student_id)

                # Check if new student already has a profile (and it's not this one)
                if (
                    hasattr(new_student, "profile")
                    and new_student.profile.id != profile.id
                ):
                    messages.error(
                        request, f"{new_student.name} already has a profile."
                    )
                else:
                    # Update profile
                    profile.student = new_student
                    profile.bio = bio
                    profile.profile_picture_url = profile_picture_url
                    profile.emergency_contact = emergency_contact
                    profile.emergency_phone = emergency_phone
                    profile.hobbies = hobbies
                    profile.achievements = achievements
                    profile.blood_group = blood_group
                    profile.parent_name = parent_name
                    profile.parent_email = parent_email
                    profile.save()
                    messages.success(request, f"Profile updated successfully!")
                    return redirect("profile_detail", id=profile.id)
            except Student.DoesNotExist:
                messages.error(request, "Selected student does not exist.")
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")

    all_students = Student.objects.all()

    return render(
        request,
        "student/profile_form.html",
        {
            "profile": profile,
            "student": student,
            "students": all_students,
            "form_type": "Update",
        },
    )


def profile_delete(request, id):
    """Delete a student's profile"""
    profile = get_object_or_404(StudentProfile, id=id)
    student = profile.student

    if request.method == "POST":
        student_name = student.name
        profile.delete()
        messages.success(request, f"Profile for {student_name} deleted successfully!")
        return redirect("profile_list")

    return render(
        request,
        "student/profile_confirm_delete.html",
        {"student": student, "profile": profile},
    )
