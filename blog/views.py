from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        return super().get_queryset()[:3]


def posts(request):
    posts_data = Post.objects.all().order_by("-date")
    return render(
        request,
        "blog/all-posts.html",
        {
            "posts": posts_data,
        },
    )


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(
        request, "blog/post-details.html", {"post": post, "post_tags": post.tags.all()}
    )


class SinglePostView(DetailView):
    template_name = "blog/post-details.html"
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()  # type: ignore
        return context
