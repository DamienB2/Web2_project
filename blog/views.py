from django.shortcuts import render, redirect
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
    #fonctionne mais redirige le user directement vers le home car le mdp n'est pas entré
    model = Post
    template_name = 'post_detail.html'  # Remplacez 'your_template_name.html' par le nom de votre modèle

    def get(self, request, *args, **kwargs):

        # Récupérer le mot de passe du formulaire
        password_from_form = self.request.GET.get('pwd')

        # Récupérer l'objet Post
        post_object = self.get_object()

        # Comparer le mot de passe
        if password_from_form == post_object.access_code:
            # Mot de passe correct, vous pouvez rediriger l'utilisateur vers la vue détaillée du message
            return redirect('post-play')
        else:
            # Mot de passe incorrect, vous pouvez rediriger l'utilisateur vers une autre page ou afficher un message d'erreur
            return redirect('post-detail')  # Remplacez 'ma_page_d_erreur' par le nom de votre page d'erreur


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
    post = Post.pk  
    return render(request, 'blog/post_play.html', {'title': 'Game', 'post': post})


def statistics(request):
    return render(request, 'blog/statistics.html', {'title': 'Statistics'})
