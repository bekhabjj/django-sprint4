from django import forms
from blog.models import Comment, Post, UserProfile


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
        model = UserProfile
        fields = ['avatar']
