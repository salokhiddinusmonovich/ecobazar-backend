import uuid

from django.db import models
from category.models import Tag, Category, Type, Color
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()




class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=25)
    quantity = models.PositiveIntegerField()
    teg = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='product_tag')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product_category')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.OneToOneField(Type, on_delete=models.SET_NULL, null=True, related_name='product_type' )
    color = models.OneToOneField(Color, on_delete=models.SET_NULL, null=True, related_name='product_color')
    weight = models.IntegerField()

    def __str__(self):
        return self.title






class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/')
    is_main = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.product.title}"


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    blog = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    star = models.IntegerField(default=0,
                               validators=[MaxValueValidator(5), MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=True)


    def __str__(self):
        try:
            return f'{self.author.name} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    class Meta:
        ordering = ['-created']


class LikedFeedback(models.Model):
    comment = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
