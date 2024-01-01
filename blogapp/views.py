from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from taggit.models import Tag
from .forms import *
# Create your views here.

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

from django.views.generic import CreateView

# new post page
class PostCreateView(CreateView):
    template_name = 'blogapp/new_post.html'
    success_url = '/posts'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)