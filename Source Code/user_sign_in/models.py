from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.first_name