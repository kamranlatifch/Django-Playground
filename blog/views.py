from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment


def post_list(request):
    """
    Display a list of all published blog posts
    """
    # Get only published posts, ordered by newest first
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    """
    Display a single post with its comments
    """
    # Get the post, or show 404 if not found
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Increment view count
    post.views += 1
    post.save(update_fields=["views"])

    # Get approved comments for this post
    comments = post.comments.filter(is_approved=True)

    # Handle comment submission (if form was submitted)
    if request.method == "POST":
        author_name = request.POST.get("author_name")
        author_email = request.POST.get("author_email")
        content = request.POST.get("content")

        if author_name and author_email and content:
            # Create new comment (not approved by default)
            Comment.objects.create(
                post=post,
                author_name=author_name,
                author_email=author_email,
                content=content,
            )
            # Redirect to refresh the page
            return redirect("post_detail", slug=slug)

    return render(
        request, "blog/post_detail.html", {"post": post, "comments": comments}
    )


def home(request):
    """Home page - redirects to blog list"""
    return redirect("post_list")
