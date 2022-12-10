from django.contrib import admin
from blogApp.models import *

class PostAdmin(admin.ModelAdmin):
    list_display=['status','title','slug','author','body','publish','created_at','modified_at']

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','mail','body','created_at','modified_at']

admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentAdmin)
