from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class Xuser(AbstractUser):
    email = models.EmailField(max_length=50,unique=True)
    dob = models.DateField(null=True,blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/',null=True,blank=True)
    display_name = models.CharField(max_length=50,null=True,blank=True)
    bio = models.TextField(blank=True)
    is_profile_complete = models.BooleanField(default=False)
    
    # following many to manny relationship
    following = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )

    class Meta:
        db_table = "xuser"

class Tweet(models.Model):
    user = models.ForeignKey(Xuser,on_delete=models.CASCADE,related_name='tweets')
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='tweet_images/',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "tweets"
        ordering = ['-created_at']
    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}....'