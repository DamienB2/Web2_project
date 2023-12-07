from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


#permet d'afficher les posts sur la page principale
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


#permet d'afficher le détail des posts quand on clique dessus
class PostDetailView(DetailView):
    model = Post


#permet de créé un nouveau post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'grid_size', 'alignment', 'is_public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#Permet d'update un post déjà existant
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'grid_size', 'alignment', 'is_public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


#Permet de supprimer un post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def PostPlay(request):
    return render(request, 'blog/post_play.html', {'title': 'Game'})


def statistics(request):
    return render(request, 'blog/statistics.html', {'title': 'Statistics'})
