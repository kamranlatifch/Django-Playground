"""
URL configuration for django_playground project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from student import views

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel
    path("silk/", include("silk.urls", namespace="silk")),  # Query profiling UI
    path("student/", views.student_list, name="student_list"),  # List all students
    path(
        "student/create/", views.student_create, name="student_create"
    ),  # Create student
    path(
        "student/<int:id>/", views.student_detail, name="student_detail"
    ),  # Student detail
    path(
        "student/<int:id>/update/", views.student_update, name="student_update"
    ),  # Update student
    path(
        "student/<int:id>/delete/", views.student_delete, name="student_delete"
    ),  # Delete student
    # Profile URLs
    path("profile/", views.profile_list, name="profile_list"),  # List all profiles
    path(
        "profile/create/",
        views.profile_create,
        name="profile_create",
    ),  # Create profile
    path(
        "profile/<int:id>/", views.profile_detail, name="profile_detail"
    ),  # Profile detail
    path(
        "profile/<int:id>/update/",
        views.profile_update,
        name="profile_update",
    ),  # Update profile
    path(
        "profile/<int:id>/delete/",
        views.profile_delete,
        name="profile_delete",
    ),  # Delete profile
]
