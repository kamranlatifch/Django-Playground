from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model
    This controls how posts appear in the Django admin panel
    """

    # What columns to show in the list view
    list_display = ("title", "is_published", "created_at", "views")

    # Add filters on the right side
    list_filter = ("is_published", "created_at")

    # Add search box
    search_fields = ("title", "content")

    # Auto-generate slug from title
    prepopulated_fields = {"slug": ("title",)}

    # Fields that can't be edited (read-only)
    readonly_fields = ("created_at", "updated_at", "views")

    # Organize fields into sections
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "content", "excerpt")}),
        ("Publishing", {"fields": ("is_published",)}),
        (
            "Statistics",
            {
                "fields": ("views", "created_at", "updated_at"),
                "classes": ("collapse",),  # Collapsible section
            },
        ),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model
    """

    list_display = ("author_name", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("author_name", "content", "post__title")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Comment", {"fields": ("post", "author_name", "author_email", "content")}),
        ("Moderation", {"fields": ("is_approved",)}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
