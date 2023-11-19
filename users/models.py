from django.db import models
from django.contrib.auth.models import User

#Si on ajoute quelque chose dans models, il doit y avoir un makemigrations dans la DB et ensuite un migrate
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    #Permet d'afficher un objet. Sans ça, affiche "Profile object"
    def __str__(self):
        return f'{self.user.username} Profile'
