from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .forms import PostForm
from .models import Post, Tag


@login_required
def index(request):
    time_since = timezone.now() - timedelta(days=3)
    post_list = (
        Post.objects.all()
        .filter(Q(author__in=request.user.following_set.all()) | Q(author=request.user))
        .filter(created_at__gte=time_since)
    )

    suggested_user_list = (
        get_user_model()
        .objects.exclude(pk=request.user.pk)
        .exclude(pk__in=request.user.following_set.all())[:3]
    )
    return render(
        request,
        "extagram/index.html",
        {"suggested_user_list": suggested_user_list, "post_list": post_list},
    )


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "포스트를 저장하였습니다.")
            return redirect(post)
    else:
        form = PostForm()

    return render(request, "extagram/post_form.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "extagram/post_detail.html", {"post": post,})


@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    # post_list = page_user.post_set.all()
    post_list = Post.objects.filter(author=page_user)
    return render(
        request,
        "extagram/user_page.html",
        {"page_user": page_user, "post_list": post_list, "is_follow": is_follow},
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, "포스팅을 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, "좋아요를 취소했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)
