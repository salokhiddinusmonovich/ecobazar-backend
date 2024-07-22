# from icecream import ic
from rest_framework import serializers
from blog.models import Comment, Tag, Blog, Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_author_name(self, obj): # noqa
        return obj.author.username


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", 'body']
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
        # fields = ["id", 'name']
        # read_only_fields = ["id"]


class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", 'name', 'order']
        read_only_fields = ["id"]


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Blog
        # fields = '__all__'
        exclude = ('tags',)


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.ReadOnlyField(source='category.name')
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogCreateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            "id", 'title', 'description', 'category', 'tags'
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data) # noqa
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            blog.tags.add(tag)
        return blog


def create_or_update_tags(tags):
    return [Tag.objects.update_or_create(pk=tag.get('id'), defaults=tag)[0].pk for tag in tags]


class BlogUpdateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = [
            "id", 'title', 'description', 'category', 'tags'
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)
        return super().update(instance, validated_data)


class CategoryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryBlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'name']
        read_only_fields = ["id"]


class CategoryBlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'name']
        read_only_fields = ["id"]