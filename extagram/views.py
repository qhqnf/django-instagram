from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import PostForm
from .models import Post, Tag


@login_required
def index(request):
    suggested_user_list = (
        get_user_model()
        .objects.exclude(pk=request.user.pk)
        .exclude(pk__in=request.user.following_set.all())[:3]
    )
    return render(
        request, "extagram/index.html", {"suggested_user_list": suggested_user_list,}
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
    # post_list = page_user.post_set.all()
    post_list = Post.objects.filter(author=page_user)
    return render(
        request,
        "extagram/user_page.html",
        {"page_user": page_user, "post_list": post_list},
    )

