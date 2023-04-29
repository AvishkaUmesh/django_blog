from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.urls import reverse

from blog.forms import CommentForm
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


class SinglePostView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),  # type: ignore
        }
        return render(request, "blog/post-details.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("blog-post-details", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),  # type: ignore
        }
        return render(request, "blog/post-details.html", context)
