from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    slug = AutoSlugField(unique=True, populate_from='title')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='featured_images/', blank=True)
    thumbnail_image = models.ImageField(upload_to='thumbnail_images/', blank=True)
    file = models.FileField(upload_to='documents/')
    


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
       return self.user
    

class Student(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name