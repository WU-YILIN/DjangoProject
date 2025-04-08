from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    manufacturing_since = models.DateField()

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    launch_date = models.DateField()
    platform = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


class Review(models.Model):
    related_models = models.ManyToManyField(Model)
    review_article = models.TextField()
    date_published = models.DateField()

    def __str__(self):
        return f"Review on {', '.join([model.model_name for model in self.related_models.all()])}"
