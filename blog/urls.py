from django.urls import path
from . import views

urlpatterns = [
    path("", views.start_page, name="blog-home"),
    path("/posts", views.posts, name="blog-posts"),
    path("/post/<slug:slug>", views.post_details, name="blog-post-details"),
]
