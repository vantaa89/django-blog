from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


class Image(models.Model):
    image = models.ImageField(upload_to="%Y-%m-%d")
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='title', null=False)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    special_post = models.BooleanField(default=False)   # about이나 main에 들어가는 특별한 글인지 여부

    def __str__(self):
        return f"{self.title}"


class News(models.Model):
    content = models.TextField(max_length=100)
    time = models.DateField()

    def __str__(self):
        return f"[{self.time}] {self.content}"

    class Meta:
        verbose_name_plural = "News"