"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path, include
from .views import *


app_name = "blog"

urlpatterns = [
    path('', main_view),
    path('about/', about_view, name="about"),
    path('posts/', PostList.as_view(), name="posts"),
    path('posts/new/', PostCreateView.as_view(), name="new_post"),
    path('post/<slug:slug>', PostView.as_view(), name="post"),
    path('post/<slug:slug>/delete/', delete_post, name="delete_post"),
    path('post/<slug:slug>/modify/', modify_post, name="modify_post"),
    path('tags/<slug:slug>', tagged, name="tagged"),
    path('images/', upload_images, name="upload_images"),
    path('markdown_preview/', markdown_preview, name="markdown_preview"),
]
