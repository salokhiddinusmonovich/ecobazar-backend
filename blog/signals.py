from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Blog


@receiver(post_delete, sender=Blog, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
    cache.delete('blog_categories')


@receiver(post_save, sender=Blog, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('blog_categories')