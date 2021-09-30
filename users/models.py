from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg' , upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' 
    def save(self,*args,**kwarg):
        super().save(*args,**kwarg)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            if img.height > 300:
                output_size = (300,(300/img.height)*img.width)
            else:
                output_size = ((300/img.width)*img.height,300)
            img.thumbnail(output_size)
            img.save(self.image.path)