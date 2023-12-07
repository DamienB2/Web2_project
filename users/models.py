from django.db import models
from django.contrib.auth.models import User
from PIL import Image

#Si on ajoute quelque chose dans models, il doit y avoir un makemigrations dans la DB et ensuite un migrate
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    symbol = models.ImageField(default='default.jpg', upload_to='symbol_pics') # Il faudrait mettre comme image par defaut l'image de profil du user

    #Permet d'afficher un objet. Sans ça, affiche "Profile object"
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        sbl = Image.open(self.symbol.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        if sbl.height > 300 or sbl.width > 300:
            output_size = (300, 300)
            sbl.thumbnail(output_size)
            sbl.save(self.symbol.path)
