from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    slug = models.SlugField(unique=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.user.username)
        super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.user.username