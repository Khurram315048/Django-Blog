from django.shortcuts import render,redirect,get_object_or_404
from blogs.models import Blog,Category
from django.contrib.auth.decorators import login_required
from dashboards.forms import CategoryForm,BlogPostForm
import uuid
from django.utils.text import slugify


@login_required(login_url='login')
def dashboard(request):
    category_count=Category.objects.all().count()
    blogs_count=Blog.objects.all().count()
    context={
        'category_count':category_count,
        'blogs_count':blogs_count,
    }
    return render(request,'dashboard/dashboard.htm',context)




def categories(request):
    return render(request,'dashboard/categories.htm')




def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')

    context={
        'form':form,
    }
    return render(request,'dashboard/add_category.htm',context)  



def edit_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request,'dashboard/edit_category.htm',context)   


def delete_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    return redirect('categories')


def posts(request):
    posts=Blog.objects.all()
    context={
        'posts':posts,
    }
    return render(request,'dashboard/posts.htm',context)    


def add_post(request):
    if request.method == 'POST':
        form=BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            base_slug=slugify(form.cleaned_data['title'])
            post.slug=f"{base_slug}-{uuid.uuid4().hex[:8]}"
            post.save()
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)

    form=BlogPostForm()
    context={
        'form':form,
        }
    return render(request,'dashboard/add_post.htm',context)





def edit_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    if request.method == 'POST':
        form=BlogPostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save()
            title=form.cleaned_data['title']
            post.slug=slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')
    form=BlogPostForm(instance=post)
    context={
        'form':form,
        'post':post
    }
    return render(request,'dashboard/edit_post.htm',context)


def delete_post(request,pk):
    post=get_object_or_404(Blog,pk=pk)
    post.delete()
    return redirect('posts')    

