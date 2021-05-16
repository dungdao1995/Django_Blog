from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    #Render built-in function aldeady return HTTPresponse in the background, 
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html', context) 

#show the blog LIST based on the ListView already exist in django
class PostListView(ListView):
    model = Post
    #Because automatically, DJango expect the blog/post_list.html, so we need to change the html file
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html 
    #set variable LIKE a LOOP for check all post
    context_object_name = 'posts'
    ordering = ['-date_posted'] #lastest blog will be showed first
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    #Because automatically, DJango expect the blog/post_list.html, so we need to change the html file
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html 
    #set variable LIKE a LOOP for check all post
    context_object_name = 'posts'
    #ordering = ['-date_posted'] #lastest blog will be showed first
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


#show the detail of a blog based on the ListView already exist in django
class PostDetailView(DetailView):
    model = Post

#Create the new Post
class PostCreateView(LoginRequiredMixin, CreateView): #LoginRequire: You need to log in before creating the new POST
    model = Post
    fields = ['title', 'content'] # the fields in the page create New: title and content

    #override the method when save the new Post
    def form_valid(self,form):
        form.instance.author = self.request.user # set author is the logged author
        return super().form_valid(form)

#updata the post
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView): 
    #LoginRequire: You need to log in before creating the new POST
    #UserPassesTestMixin: check need to have the same author
    model = Post
    fields = ['title', 'content'] # the fields in the page create New: title and content

    #override the method when save the new Post
    def form_valid(self,form):
        form.instance.author = self.request.user # set author is the logged author
        return super().form_valid(form)

    #check the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: #current author is the post author
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/' #when deleting successfully, return to the home page
    #check the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: #current author is the post author
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'}) 