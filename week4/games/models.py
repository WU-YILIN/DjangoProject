from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=20)
class Games(models.Model):
    title = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    platform = models.CharField(max_length=50,default='null')
    label_tags = models.ManyToManyField(Tags)
    slug = models.SlugField(max_length=150,default='null')
class Review(models.Model):
    game = models.ForeignKey(Games,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=150,default='null')
