from django.contrib import admin

# Register your models here.
from oneToMany.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "author__name")
