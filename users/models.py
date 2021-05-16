from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) # when delete the User => will delete the profile 
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics') #save it to the profile_pics folder, but it is the children folder in the Media

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs)
        #resize imgae
        img = Image.open(self.image.path)

        if(img.height > 300 or img.width >300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


