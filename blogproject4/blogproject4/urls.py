"""blogproject4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from blogApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tag/<slug:tag_slug>/',views.post_list_view,name='post_list_by_tag_name'),
    path('',views.post_list_view),
    path('detail/<int:id>/',views.post_detail_view),
    path('sharemail/<int:id>/',views.sharemail),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signup/',views.Signup),
    path('verification/',views.Verify)
]
