from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Configurations to manage from the admin view.
    """

    # To see in admin posts page
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}  # To autofill slug with title
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Configurations to manage from the admin view.
    """

    list_display = ("name", "email", "post", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")
