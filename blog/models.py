from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max

User = get_user_model()




class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(TimeStampModel):
    name = models.CharField(max_length=20)
    order = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_order = Tag.objects.aggregate(Max('order'))['order__max'] # noqa
            self.order = (max_order + 1) if max_order is not None else 1
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(TimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Blog(TimeStampModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    file = models.ImageField(upload_to='blogs/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(TimeStampModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=1000)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body