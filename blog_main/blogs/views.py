from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Blog,Category
from django.db.models import Q



def posts_by_category(request,category_id):
    posts=Blog.objects.filter(status='Published',category=category_id)
    try:

        category=Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    
    context={
        'posts':posts,
        'category':category,
    }
    return render(request,'posts_by_category.htm',context)


def blogs(request,slug):
    single_blog=get_object_or_404(Blog,slug=slug,status='Published')
    context={
        'single_blog':single_blog,
    }
    return render(request,'blogs.htm',context)


def search(request):
    keyword=request.GET.get('keyword')
    blogs=Blog.objects.filter(Q(title__icontains=keyword) |Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword)
                              ,status='Published')
    context={
        'blogs':blogs,
        'keyword':keyword,
    }
    return render(request,'search.htm',context)