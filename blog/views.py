from django.shortcuts import render,get_object_or_404
#from django.contrib.auth.decorators import login_required only used for function based Views
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from.models import post
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                    DetailView, 
                                    CreateView,
                                    UpdateView,
                                    DeleteView                                    
)
#from django.http import HttpResponse


def home(request):
    context = {
        'posts' : post.objects.all(),
        'title' : " -Home"
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = post
    template_name='blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = post

#@login_required only use decorator for FUNCTION based View for class bsed  views use LoginRequiredMixin class

class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UserPostListView(ListView):
    model = post
    template_name='blog/user_post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return post.objects.filter(author = user ).order_by('-date_posted')




class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = post
    fields = ['title','content']
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request , 'blog/about.html', {'title' : ' - About'} )


# Create your views here.
