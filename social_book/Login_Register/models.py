from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from django.core import validators
from django.utils import timezone

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=30, null=False, blank=False)
    # last_name = models.CharField(max_length=30, null=False, blank=False)
    public_visibility = models.BooleanField(default=True)
    date_of_birth = models.DateField(validators=[
        validators.MinValueValidator(
            timezone.datetime(1900, 1, 1).date(),
            'Please enter a valid date of birth.'
        ),
        validators.MaxValueValidator(
            timezone.now().date(),
            'Please enter a valid date of birth'
        ),
    ], null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveIntegerField(editable=False, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth', 'city', 'state', 'public_visibility']

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    

class UploadedFiles(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_published = models.PositiveIntegerField()
    file = models.FileField(upload_to='uploads/')
    is_pdf = models.BooleanField(default=False)

    def __str__(self):
        return self.title