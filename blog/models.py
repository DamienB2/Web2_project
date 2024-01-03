import random

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#makemigrations -> sqlmigrate blog 0001 -> migrate

def generate_random_access_code():
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(6))


class Post(models.Model):
    title = models.CharField(max_length=100)
    grid_size = models.IntegerField(default=3, validators=[MinValueValidator(3)])
    alignment = models.IntegerField(default=3, validators=[MinValueValidator(3)])
    is_public = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    is_surrendered = models.BooleanField(default=False)
    access_code = models.CharField(max_length=6, default=generate_random_access_code)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='opponent')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='winnerOfGame')
    played_positions = models.JSONField(default=list)
    players = models.CharField(max_length=1, default="X")


    def add_position(self, position):
        # Méthode pour ajouter une position à la liste
        self.played_positions.append(position)
        self.save()

    def add_opponent(self, opponent):
        self.opponent = opponent
        self.save()

    def add_winner(self, winner):
        self.winner = winner
        self.save()

    def set_finished(self):
        self.is_finished = True
        self.save()

    def change_player(self, players):
        self.players = players
        self.save()

    def surrendered(self):
        self.is_surrendered = True
        self.save()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})