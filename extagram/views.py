from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm
from .models import Tag


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
            return redirect("/")  # TODO get_absolute_url
    else:
        form = PostForm()

    return render(request, "extagram/post_form.html", {"form": form})
