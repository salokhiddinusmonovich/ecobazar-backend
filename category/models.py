from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/")

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=20)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name




class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StockStatus(models.Model):
    numbers = models.PositiveIntegerField(default=0)

