from django import template
from blogApp.models import Post

register=template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blogApp/latestposts.html')
def showlatestposts(count=2):
    return {'latest_posts':Post.objects.all().order_by('-publish')[:count]}
