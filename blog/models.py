from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    """
    Blog Post Model
    This represents a blog post in our database.
    Each field becomes a column in the database table.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200, unique=True, help_text="URL-friendly version of title"
    )
    content = models.TextField()
    excerpt = models.CharField(
        max_length=300, blank=True, help_text="Short summary (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=False, help_text="Check to publish this post"
    )
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]  # Newest posts first

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to view this post"""
        return reverse("post_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    """
    Comment Model
    Comments belong to a Post (ForeignKey relationship)
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(
        default=False, help_text="Approve to show on website"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"
