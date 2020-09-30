from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.clenaed_data.get("email")
        if email:
            qs = User.objects.filter(email=email)
            if qs.exist():
                raise forms.ValidationError("이미 존재하는 이메일입니다.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "website_url",
            "bio",
            "phone_number",
            "gender",
        ]
