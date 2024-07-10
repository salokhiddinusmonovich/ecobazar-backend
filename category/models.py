from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="product/")

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

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


