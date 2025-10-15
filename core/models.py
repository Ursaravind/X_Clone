from django.db import models
from django.contrib.auth.models import AbstractUser

class Xuser(AbstractUser):
    email = models.EmailField(max_length=50)
    dob = models.DateField(null=True,blank=True)

    class Meta:
        db_table = "xuser"

