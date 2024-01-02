from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# permet d'afficher les posts sur la page principale
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


# permet de créé un nouveau post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'grid_size', 'alignment', 'is_public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Permet d'update un post déjà existant
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


# Permet de supprimer un post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def PostPlay(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if request.method == 'POST':

        password_from_form = request.POST.get('pwd')

        # Comparer le mot de passe
        if password_from_form == post.access_code:
            # si la personne qui rejoins n'est pas l'author
            if user != post.author:
                # si il n'y a pas encore d'opposant
                if post.opponent is None:
                    post.add_opponent(user)
                elif post.opponent == user:
                    return redirect('post-play', post.pk)
                else:
                    messages.warning(request, f'The game is full.')
                    return redirect('post-detail', post.pk)

            return redirect('post-play', post.pk)
        else:
            messages.warning(request, f'You entered the wrong password.')
            return redirect('post-detail', post.pk)

    return render(request, 'blog/post_detail.html', {'title': 'Details', 'post': post})


def play(request, pk):
    post = Post.objects.get(pk=pk)
    tiles = post.grid_size

    if request.method == 'POST':
        position_id = request.POST.get('position_id')
        players = request.POST.get('players')
        surrender = request.POST.get('surrender')
        leave = request.POST.get('leave')
        winner = request.POST.get('winner')

        if leave:
            return redirect('blog-home')

        if winner != "":
            if winner == 'X':
                post.add_winner(post.author)
            else:
                post.add_winner(post.opponent)

        if surrender:
            surrender_player = request.user

            if post.winner is None:
                if surrender_player == post.author:
                    post.add_winner(post.opponent)
                else:
                    post.add_winner(post.author)

                messages.warning(request, "You surrendered the game")

                return redirect('blog-home')
            else:
                messages.warning(request, "You won because your opponent left the game")
                return redirect('blog-home')

        if position_id:
            try:
                post.add_position(position_id)
                post.change_player(players)
                return JsonResponse({'status': 'success'})
            except Post.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Post not found'})
        else:
            return JsonResponse({'played_positions': post.played_positions, 'players': post.players})

    return render(request, 'blog/post_play.html', {'title': 'Game', 'nbCases': range(tiles), 'post': post})


def statistics(request):
    grid_size = 3 #default value
    alignment = 3 #default value

    context = {
        'posts': Post.objects.all(),
        'title': 'Statistics',
        'Ranked_posts': generate_ranked_posts(grid_size, alignment)
    }

    if request.method == 'POST':
        grid_size = int(request.POST.get('grid'))
        alignment = int(request.POST.get('Alignment'))

        context['Ranked_posts'] = generate_ranked_posts(grid_size, alignment)

    return render(request, 'blog/statistics.html', context)

def generate_ranked_posts(grid_size, alignment):
    matching_posts = Post.objects.filter(grid_size=grid_size, alignment=alignment)
    ranked_posts = matching_posts.values('winner__username').annotate(wins_count=Count('winner')).order_by('-wins_count')
    return ranked_posts


