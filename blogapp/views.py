from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

# main 페이지
def main_view(request):
    post = Post.objects.filter(title="about").first()
    post_list = Post.objects.filter(special_post=False).order_by('-created_at')[:4]
    return render(
        request, 
        'blogapp/index.html',
        {
            'post': post,
            'post_list': post_list,
        }
    )

# about 페이지
def about_view(request):
    post = Post.objects.filter(title="cv").first()
    return render(
        request, 
        'blogapp/about.html',
        {'post': post}
    )

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
