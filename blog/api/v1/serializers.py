from rest_framework import serializers

from blog.models import Blog, Comment
from category.models import BlogCategory


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    class Meta:
        model = Blog
        fields = ['pk',
                  'title',
                  'description',
                  'file',
                  'author',
                  'tag',
                  'created_at',
                  'updated_at',
                  'is_published']

# class BlogCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Blog
#         fields = ['title',
#                   'description',
#                   # 'file',
#                   'is_published']

class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Comment
        fields = ['pk', 'body', 'blog', 'author']

class BlogCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name']

class BlogDetailSerializer(serializers.ModelSerializer):
    category = BlogCategoryNameSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['pk',
                  'title',
                  'description',
                  'file',
                  'author',
                  'tag',
                  'comments',
                  'category']

    def get_comments(self, obj):
        feedback = Comment.objects.filter(products=obj)
        serializer = CommentListSerializer(feedback, many=True)
        return serializer.data
