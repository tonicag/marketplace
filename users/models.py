from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager  
# Create your models here.




class CustomUserManagement(BaseUserManager):
    def create_user(self,email,password,is_influencer, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,is_influencer=is_influencer,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_influencer', False)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_influencer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=255,default='ionci')
    USERNAME_FIELD = 'email'

    objects = CustomUserManagement()

    REQUIRED_FIELDS = ['is_influencer']