from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
    
    )

from . import views
urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'), #pk:primary key blog/post/1: blog 1 has the pk = 1
    path('post/new/', PostCreateView.as_view(), name = 'post-create'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'), #still using the pk to specify the post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'), #still using the pk to specify the post
    path('about/', views.about, name = 'blog-about'),
]


