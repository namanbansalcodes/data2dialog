from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class AppUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)


class AppUser(AbstractUser):
    
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, null=True)
    company = models.CharField(max_length=60, null=True)
    databases = models.ManyToManyField('Database')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = AppUserManager()
    
    
    
class Database(models.Model):
    name = models.CharField(max_length=50, blank=False)
    database_type = models.CharField(max_length=50)
    connectors = models.JSONField(blank=False)
    chat = models.ManyToManyField('Chat')

class Chat(models.Model):
    convos = models.JSONField(blank=False)