from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="blog-home"),
    path("posts", views.AllPostsView.as_view(), name="blog-posts"),
    path("post/<slug:slug>", views.SinglePostView.as_view(), name="blog-post-details"),
]
