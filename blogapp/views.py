from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from taggit.models import Tag
from .forms import *
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import markdown as md
import re

# main 페이지
def main_view(request):
    main_post = Post.objects.filter(title="main").first()
    post_list = Post.objects.filter(special_post=False).order_by('-created_at')[:4]
    news_list = News.objects.order_by('-time')[:3]
    return render(
        request, 
        'blogapp/index.html',
        {
            'post': main_post,
            'post_list': post_list,
            'news_list': news_list,
        }
    )

# about 페이지
def about_view(request):
    post = Post.objects.filter(title="about").first()
    return render(
        request, 
        'blogapp/about.html',
        {'post': post}
    )

# 개별 post 페이지
class PostView(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'

class PostList(ListView):
    model = Post
    template_name = 'blogapp/posts.html'

    paginate_by = 10

    def get_queryset(self):
        new_context = Post.objects.filter(special_post=False).order_by('-created_at')
        return new_context

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        return context

# tag page
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'blogapp/tags.html', context)


# new post page
class PostCreateView(CreateView):
    template_name = 'blogapp/editor.html'
    success_url = '/posts'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post'] = True
        context['post_target'] = reverse('blog:new_post')
        return context
    

@login_required
def modify_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('blog:posts')
            return redirect('blog:modify_post')
        else:
            form = PostForm(instance=post)
            return render(request,
                'blogapp/editor.html', 
                {
                    'new_post': False, 
                    'post': post, 
                    'form': form,
                    'post_target': reverse('blog:modify_post', args=[post.slug])
                })
    return redirect('posts:index')


# delete post
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Get your current post

    if request.method == 'POST':         # If method is POST,
        post.delete()                     # delete the post.
        return redirect('/posts')             # Finally, redirect to the homepage.

    return render(request, 'blogapp/post_detail.html', {'post': post})

@csrf_exempt
def upload_images(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_file = request.FILES.getlist('images')[0]
        image_instance = Image(image=uploaded_file)
        image_instance.save()
        return JsonResponse({'message': 'File(s) uploaded successfully', 'files':str(uploaded_file), 'url': image_instance.image.url})
    else:
        return JsonResponse({'message': 'No files received'}, status=400)


def markdown_preview(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        content = re.sub(r'\$(.*)\$', lambda match: match.group(0).replace('_', '<mathsubscript>'), content)    
        html_content = md.markdown(content, extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
            ])
        html_content = html_content.replace('<mathsubscript>', '_')
            
        return JsonResponse({'success': True, 'html_content': html_content})
    else:
        return JsonResponse({'success': False}, status=400)