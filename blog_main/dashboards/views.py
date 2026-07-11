from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import  BlogPostForm,CategoryForm,AddUserForm,EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
import logging
from django.contrib import messages



logger=logging.getLogger(__name__)

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='login')(login_required(login_url='login')(view_func))


@staff_required
def dashboard(request):
    category_count=Category.objects.all().count()
    blogs_count=Blog.objects.all().count()
    context={
        'category_count':category_count,
        'blogs_count':blogs_count,
    }
    return render(request,'dashboard/dashboard.htm',context)


@staff_required
def categories(request):
    categories=Category.objects.all().order_by('created_at')
    context={
        'categories':categories
        }
    return render(request,'dashboard/categories.htm',context)



@staff_required
def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category added successfully!')
            return redirect('categories')

    context={
        'form':form,
    }
    return render(request,'dashboard/add_category.htm',context)  

@staff_required
def edit_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('categories')

    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request,'dashboard/edit_category.htm',context)   



@staff_required
def delete_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category deleted successfully!')
    return redirect('categories')

  


@staff_required
def posts(request):
    posts=Blog.objects.all().select_related('author','category')
    paginator=Paginator(posts,10)  
    page=request.GET.get('page',1)
    page_obj=paginator.get_page(page)
    
    context={
        'page_obj':page_obj
        }
    return render(request,'dashboard/posts.htm',context)


@staff_required
def add_post(request):
    if request.method == 'POST':
        form=BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            base_slug=slugify(form.cleaned_data['title'])
            post.slug=f"{base_slug}-{uuid.uuid4().hex[:8]}"
            post.save()
            messages.success(request,'Post added successfully!')
            return redirect('posts')
        else:
            logger=logging.getLogger(__name__)
            logger.error(f'Form validation failed:{form.errors}')

    form=BlogPostForm()
    context={
        'form':form,
        }
    return render(request,'dashboard/add_post.htm',context)






@staff_required
def edit_post(request, pk):
    post=get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form=BlogPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save() 
            messages.success(request,'Post Updated successfully!') 
            return redirect('posts')
    
    form=BlogPostForm(instance=post)
    context={
        'form':form,
        'post':post
    }
    return render(request,'dashboard/edit_post.htm',context)



@staff_required
def delete_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    if request.method=='POST':
        post_title=post.title  
        post.delete()
        messages.success(request,f'Post "{post_title}" deleted successfully!')
        logger.info(f'Post deleted: {post_title} by user {request.user}')
        return redirect('posts')
    
    messages.warning(request,'Invalid request method. Please use the delete button in the table.')
    return redirect('posts')   



@staff_required
def users(request):
    all_users=User.objects.all().order_by('-date_joined')
    paginator=Paginator(all_users, 20)
    page=request.GET.get('page', 1)
    page_obj=paginator.get_page(page)
    
    context={
        'page_obj':page_obj,
        }
    return render(request,'dashboard/users.htm',context)


@staff_required
def add_user(request):
    if request.method == 'POST':
        form=AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User added successfully!')
            return redirect('users')
        else:
            logger=logging.getLogger(__name__)
            logger.error(f'User form validation failed: {form.errors}')

    form=AddUserForm()
    context={
        'form':form,
    }
    return render(request,'dashboard/add_user.htm',context)    


@staff_required
def edit_user(request, pk):
    user=get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form=EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'User updated successfully!')
            return redirect('users')

    form=EditUserForm(instance=user)
    context={
        'form':form,
    }
    return render(request,'dashboard/edit_user.htm',context)


@staff_required
def delete_user(request,pk):
    user=get_object_or_404(User,pk=pk)
    if request.method == 'POST':
        username=user.username  
        user.delete()
        messages.success(request,f'User "{username}" deleted successfully!')
        logger.info(f'User deleted: {username} by admin {request.user}')
        return redirect('users')
    
    messages.warning(request,'Invalid request method. Please use the delete button in the table.')
    return redirect('users')  