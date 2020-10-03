from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.shortcuts import resolve_url
from django.db import models

# Create your models here.


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "Male", "Male"
        FEMALE = "Female", "Female"

    follower_set = models.ManyToManyField("self", blank=True)
    following_set = models.ManyToManyField("self", blank=True)

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
        max_length=13,
        blank=True,
    )
    gender = models.CharField(choices=GenderChoices.choices, max_length=6, blank=True)
    avatar = models.ImageField(
        blank=True,
        upload_to="accounts/profile/%Y/%m/%d",
        help_text="48px * 48px 이하의 png/jpg 이미지를 올려주세요",
    )  # django-imagekit 활용 가능

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)

    """
    def send_welcome_email(self):
        title = render_to_string("accounts/welcome_email_title.txt", {"user": self,})
        content = render_to_string("accounts/welcome_email_content.txt", {"user": self})
        sender = "welcome@instagram.com"
        send_mail(title, content, sender, [self.email], fail_silently=False)
    """
