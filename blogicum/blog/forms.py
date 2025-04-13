from django import forms
from blog.models import Comment, Post, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'author': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'author' in self.fields:
            self.fields['author'].disabled = True


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
