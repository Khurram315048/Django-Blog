from django.core.checks import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Blog,Category,Comment,Like
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator



def posts_by_category(request,category_id):
    posts=Blog.objects.filter(status='Published',category=category_id)
    try:

        category=Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return redirect('home')
    
    context={
        'posts':posts,
        'category':category,
    }
    return render(request,'posts_by_category.htm',context)


def blogs(request,slug):
    single_blog=get_object_or_404(Blog,slug=slug,status='Published')
    if request.method=='POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
    comment_text=request.POST.get('comment', '').strip()

    if not comment_text:
        messages.error(request,'Comment cannot be empty')
        return HttpResponseRedirect(request.path_info)
    
    comments=Comment.objects.create(
        user=request.user,
        blog=single_blog,
        comment=comment_text
    )
    
    # if request.method=='POST':
    #     comment=Comment()

    #     if not request.user.is_authenticated:
    #         return redirect('login')
    #     comment.user=request.user
    #     comment.blog=single_blog
    #     comment.comment=request.POST['comment']
    #     comment.save()
    #     return HttpResponseRedirect(request.path_info)
    
    comments=Comment.objects.filter(blog=single_blog)
    comment_count=comments.count()

    context={
        'single_blog':single_blog,
        'comments':comments,
        'comment_count':comment_count,
    }
    return render(request,'blogs.htm',context)


# def search(request):
#     keyword=request.GET.get('keyword')
#     blogs=Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword)
#                               ,status='Published')
#     context={
#         'blogs':blogs,
#         'keyword':keyword,
#     }
#     return render(request,'search.htm',context)


def search(request):
    keyword=request.GET.get('keyword', '').strip()
    if not keyword or len(keyword) < 2:
        messages.warning(request,'Please enter at least 2 characters')
        return redirect('home')
    
    blogs=Blog.objects.filter(
        Q(title__icontains=keyword) | 
        Q(short_description__icontains=keyword) |
        Q(blog_body__icontains=keyword),
        status='Published'
    ).select_related('author', 'category')
    
    paginator=Paginator(blogs,10)
    page=request.GET.get('page',1)
    page_obj=paginator.get_page(page)
    context={
        'page_obj':page_obj,
        'keyword':keyword,
    }
    
    return render(request,'search.htm',context)






@login_required(login_url='login')
def toggle_like(request,slug):
    blog=get_object_or_404(Blog,slug=slug,status='Published')
    like,created=Like.objects.get_or_create(user=request.user, blog=blog)
    if not created:
        like.delete()
        liked=False
    else:
        liked=True
    return JsonResponse(
        {
            'liked': liked,
            'count': blog.likes.count()
         })
