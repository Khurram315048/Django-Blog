from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Category,Blog
from .forms import RegisterationForm,UserBlogPostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from blogs.models import Blog, Comment, Like,Tag
from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
import logging
from django.db.models import Count, Prefetch



class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')


# @login_required(login_url='login')
# def profile(request):
#     my_blogs=Blog.objects.filter(author=request.user)
#     my_comments=Comment.objects.filter(user=request.user)
#     total_likes_received=Like.objects.filter(blog__author=request.user).count()
#     context={
#         'my_blogs_count':my_blogs.count(),
#         'my_comments_count':my_comments.count(),
#         'total_likes_received':total_likes_received,
#     }
#     return render(request,'profile/overview.htm',context)



@login_required(login_url='login')
def profile(request):
    my_blogs=Blog.objects.filter(author=request.user).select_related('category', 'author')
    
    my_comments=Comment.objects.filter(user=request.user).select_related('blog', 'user')
    
    likes_count=Like.objects.filter(blog__author=request.user).count()
    
    context={
        'my_blogs_count':my_blogs.count(),
        'my_comments_count':my_comments.count(),
        'total_likes_received':likes_count,
    }
    return render(request,'profile/overview.htm', context)



@login_required(login_url='login')
def profile_blogs(request):
    my_blogs=Blog.objects.filter(author=request.user).order_by('-created_at')
    context={
        'my_blogs':my_blogs,
    }
    return render(request,'profile/blogs.htm',context)


@login_required(login_url='login')
def profile_add_blog(request):
    if request.method=='POST':
        form=UserBlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            base_slug=slugify(form.cleaned_data['title'])
            post.slug=f"{base_slug}-{uuid.uuid4().hex[:8]}"
            post.save()
            form.save_m2m()  
            return redirect('profile_blogs')
    else:
        form=UserBlogPostForm()

    context={
        'form':form,
    }    
    return render(request,'profile/add_blog.htm',context)


@login_required(login_url='login')
def profile_edit_blog(request,pk):
    post=get_object_or_404(Blog, pk=pk,author=request.user)
    if request.method=='POST':
        form=UserBlogPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile_blogs')
    else:
        form=UserBlogPostForm(instance=post)

    context={
        'form':form,
        'post':post,
    }    
    return render(request,'profile/edit_blog.htm',context)


@login_required(login_url='login')
def profile_delete_blog(request,pk):
    post=get_object_or_404(Blog,pk=pk,author=request.user)   
    post.delete()
    return redirect('profile_blogs')


@login_required(login_url='login')
def profile_comments(request):
    my_comments=Comment.objects.filter(user=request.user).order_by('-created_at')
    my_likes=Like.objects.filter(user=request.user).select_related('blog')
    my_blog_tags=Tag.objects.filter(blogs__author=request.user).distinct()
    context={
        'my_comments':my_comments,
        'my_likes':my_likes,
        'my_blog_tags':my_blog_tags,
    }
    return render(request,'profile/comments.htm',context)


@login_required(login_url='login')
def profile_settings(request):
    if request.method=='POST':
        form=ProfileSettingsForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form=ProfileSettingsForm(instance=request.user)

    context={
        'form':form,
    }    
    return render(request,'profile/settings.htm',context)




def home(request):
    
    featured_posts=Blog.objects.filter(is_featured=True,status='Published').order_by('updated_at')
    posts=Blog.objects.filter(is_featured=False,status='Published')
    logger=logging.getLogger(__name__)
    logger.info(f"Retrieved {len(posts)} posts")
    logger.error(f'Form is invalid: {forms.errors}')
    context={
        'featured_posts':featured_posts,
        'posts':posts,
    }
    return render(request,'home.htm',context)


def register(request):
    if request.method=='POST':
        form=RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:    
        form=RegisterationForm()

    context={
        'form':form,
    }
    return render(request,'register.htm',context)




def login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                if user.is_staff:
                    return redirect('dashboard')
                return redirect('profile') 

    form=AuthenticationForm()
    context={
        'form':form,
    }
    return render(request,'login.htm',context)




def logout(request):
    auth.logout(request)
    return redirect('home')
