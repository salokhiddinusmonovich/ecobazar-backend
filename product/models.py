import uuid
from django.db import models
from category.models import Tag, ProductCategory, Type, Color
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()

class StarModels(models.Model):
    star = models.IntegerField(default=0,
                               validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return str(self.star)

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    title = models.CharField(max_length=100)
    description = models.TextField()
    teg = models.ManyToManyField(Tag)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='products')
    discount = models.IntegerField(default=100)
    rating = models.ForeignKey(StarModels, on_delete=models.SET_NULL, null=True, related_name='products')
    weight = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images_set')
    image = models.ImageField(upload_to='product/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title}"

class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='feedback')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    star = models.ForeignKey(StarModels, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
