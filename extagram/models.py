import re
from django.conf import settings
from django.urls import reverse
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_post_set",
    )
    photo = models.ImageField(upload_to="extagram/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField("Tag", blank=True)
    location = models.CharField(max_length=100)
    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="like_post_set"
    )

    def get_absolute_url(self):
        return reverse("extagram:post_detail", args=[self.pk])

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([\w\d]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def is_like_user(self, user):
        return self.like_user_set.all().filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-id"]


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ["-id"]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
