from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#makemigrations -> sqlmigrate blog 0001 -> migrate
class Post(models.Model):
    title = models.CharField(max_length=100)
<<<<<<< Updated upstream
    content = models.TextField()
=======
    grid_size = models.IntegerField(default=3)
    alignment = models.IntegerField(default=3)
    is_public = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    access_code = models.CharField(max_length=6, default=generate_random_access_code)
>>>>>>> Stashed changes
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})