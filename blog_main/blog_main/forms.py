from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blogs.models import Blog
from django import forms

class RegisterationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('email','username','password1','password2')
    





class UserBlogPostForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=('title','category','tags','featured_image','short_description','blog_body')
        