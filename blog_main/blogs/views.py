from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Blog,Category



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
