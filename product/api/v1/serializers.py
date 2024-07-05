from rest_framework import serializers

from product.models import Product, Feedback, Images, StarModels, ProductCategory
from category.models import Color, StockStatus, Tag, Type
from user.models import User

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['pk', 'image', 'name']

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    rating = serializers.CharField(source='rating.star')

    class Meta:
        model = Product
        fields = ['pk', 'title', 'price', 'discount', 'main_image', 'rating']

    def get_main_image(self, obj):
        main_image = obj.images_set.first()
        if main_image and main_image.image:
            return main_image.image.url
        return "No image"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['pk', 'image']

class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'teg']

class FeedbackListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Feedback
        fields = ['id', 'star', 'body', 'products', 'author']

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['star', 'body', 'products']

class FeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['body', 'star']

class ProductCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategoryNameSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    rating = serializers.CharField(source='rating.star')

    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'price', 'discount', 'category', 'type', 'stock_status', 'comments', 'images', 'rating']

    def get_images(self, obj):
        images = Images.objects.filter(product=obj)
        serializer = ImageSerializer(images, many=True)
        return serializer.data

    def get_comments(self, obj):
        feedback = Feedback.objects.filter(products=obj)
        serializer = FeedbackListSerializer(feedback, many=True)
        return serializer.data
