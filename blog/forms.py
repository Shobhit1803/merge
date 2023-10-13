from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Tag
from .models import Comment
from .models import User



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tag', 'featured_image', 'thumbnail_image')

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','phone_number','image', 'email', 'password', 're_password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'image', 'bio', 'phone_number']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'email', 'text')


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'file')

class FileEditForm(forms.Form):
    new_content = forms.CharField(widget=forms.Textarea)