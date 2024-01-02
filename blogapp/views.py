from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *
from taggit.models import Tag
from .forms import *
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

# delete post
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