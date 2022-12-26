from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password):
        user = self.create_user(
            email = email,
            password = password
        )
        user.admin = True
        user.superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('Email Address', max_length=220, unique=True)
    phone_number = models.CharField(max_length=50)

    # required fields
    is_active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    superadmin = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.superadmin

    def __str__(self):
        return self.email