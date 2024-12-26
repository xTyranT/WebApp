from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, avatar=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if self.model.objects.filter(email=email).exists():
            raise ValueError('A user with that email already exists')
        if self.model.objects.filter(username=username).exists():
            raise ValueError('A user with that username already exists')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            avatar = avatar
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    avatar = models.URLField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()