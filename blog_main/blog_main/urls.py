"""
URL configuration for blog_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings 
from blogs import views as BlogsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('profile/',views.profile,name='profile'),
    path('profile/blogs/', views.profile_blogs, name='profile_blogs'),
    path('profile/blogs/add/', views.profile_add_blog, name='profile_add_blog'),
    path('profile/blogs/edit/<int:pk>/', views.profile_edit_blog, name='profile_edit_blog'),
    path('profile/blogs/delete/<int:pk>/', views.profile_delete_blog, name='profile_delete_blog'),
    path('profile/comments/', views.profile_comments, name='profile_comments'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('',views.home,name='home'),
    path('category/', include('blogs.urls')),
    path('blogs/<slug:slug>/',BlogsView.blogs,name='blogs'),
    path('blogs/search/',BlogsView.search,name='search'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',include('dashboards.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
