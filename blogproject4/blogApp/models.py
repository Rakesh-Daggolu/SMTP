from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')

class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default='draft')
    title=models.CharField(max_length=30)
    slug=models.SlugField()
    author=models.ForeignKey(User,related_name="post",on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    objects=PostManager()
    tags=TaggableManager()         #we have Tag table in libraries and TaggleManagers also

class Comments(models.Model):
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    mail=models.EmailField()
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
