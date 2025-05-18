from django.db import models

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=20)
    related_tags = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name  # 让 `name` 字段作为对象的友好表示

class Game(models.Model):
    title = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    platform = models.CharField(max_length=50,default='null')
    label_tags = models.ManyToManyField(Tags)
    slug = models.SlugField(max_length=150,default='null')
    def __str__(self):
        return self.title  #

class Review(models.Model):
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=150,default='null')

    def __str__(self):
        return str(self.game)  # 显示关联的游戏标题



