from django import forms
from django.contrib.auth import get_user_model
from blog.models import Comment, Post

User = get_user_model()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        if args and not isinstance(args[0], dict):
            user_instance = args[0]
            args = args[1:]
            kwargs["instance"] = user_instance
        else:
            user = kwargs.pop("user", None)
            if user is not None:
                kwargs["instance"] = user
        super().__init__(*args, **kwargs)
