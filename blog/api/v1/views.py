from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from blog.api.v1 import serializers
from blog.api.v1.permissions import IsAuthor
from blog.api.v1.serializers import BlogCreateSerializer
from blog.models import Comment, Blog, Tag, Category


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        tags = cache.get('blog_tags')
        if tags is None:
            tags = Tag.objects.all()  # noqa
            serializer = self.serializer_class(tags, many=True)
            cache.set('blog_tags', serializer.data)  # Store serialized data in cache
            return tags
        else:
            # Create a list of Tag objects from the cached data
            tags = [Tag(**item) for item in tags]
            # Use the Django model manager to create a queryset from the list
            return Tag.objects.filter(id__in=[tag.id for tag in tags])  # noqa

    @swagger_auto_schema(operation_id='listTag', tags=['Tag'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagDetailAPIView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'blog_tag_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'blog_tag_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Tag(**obj)  # Convert cached data back to Tag object
            return obj

    @swagger_auto_schema(operation_id='retrieveTag', tags=['Tag'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagCreateAPIView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagCreateSerializer

    @swagger_auto_schema(operation_id='createTag', tags=['Tag'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            cache.delete('blog_tags')
        return response


class TagUpdateAPIView(generics.UpdateAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagUpdateSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='updateTag', tags=['Tag'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a tag is updated
            cache.delete('blog_tags')
            pk = kwargs.get('pk')
            cache.delete(f'blog_tag_{pk}')
        return response

    @swagger_auto_schema(operation_id='updateTag', tags=['Tag'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a tag is updated
            cache.delete('blog_tags')
            pk = kwargs.get('pk')
            cache.delete(f'blog_tag_{pk}')
        return response


class TagDeleteAPIView(generics.DestroyAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        operation_id='deleteTag',
        tags=['Tag'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a tag is deleted
        cache.delete('blog_tags')
        cache.delete(f'blog_tag_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()  # noqa
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        comments = cache.get('blog_comments')
        if comments is None:
            comments = Comment.objects.all()  # noqa
            serializer = self.serializer_class(comments, many=True)
            cache.set('blog_comments', serializer.data)  # Store serialized data in cache
            return comments
        else:
            # Create a list of Category objects from the cached data
            comments = [Comment(**item) for item in comments]
            # Use the Django model manager to create a queryset from the list
            return Comment.objects.filter(id__in=[comment.id for comment in comments])  # noqa

    @swagger_auto_schema(operation_id='listComment', tags=['Comment'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()  # noqa
    serializer_class = serializers.CommentSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'blog_comment_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'blog_comment_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Comment(**obj)  # Convert cached data back to Comment object
            return obj

    @swagger_auto_schema(operation_id='retrieveComment', tags=['Comment'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()  # noqa
    serializer_class = serializers.CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(operation_id='createComment', tags=['Comment'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new comment is created
            cache.delete('blog_comments')
        return response


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()  # noqa
    serializer_class = serializers.CommentUpdateSerializer
    permission_classes = (IsAuthor,)

    @swagger_auto_schema(operation_id='updateComment', tags=['Comment'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a comment is updated
            cache.delete('blog_comments')
            pk = kwargs.get('pk')
            cache.delete(f'blog_comment_{pk}')
        return response

    @swagger_auto_schema(operation_id='updateComment', tags=['Comment'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a comment is updated
            cache.delete('blog_comments')
            pk = kwargs.get('pk')
            cache.delete(f'blog_comment_{pk}')
        return response


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()  # noqa
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthor,)

    @swagger_auto_schema(
        operation_id='deleteComment',
        tags=['Comment'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a comment is deleted
        cache.delete('blog_comments')
        cache.delete(f'blog_comment_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()  # noqa
    serializer_class = serializers.BlogListSerializer
    search_fields = ['title']

    # def get_queryset(self):
    #     posts = cache.get('blog_posts')
    #     ic(posts)
    #     if posts is None:
    #         posts = Blog.objects.all()  # noqa
    #         serializer = self.serializer_class(posts, many=True)
    #         cache.set('blog_posts', serializer.data)  # Store serialized data in cache
    #         return posts
    #     else:
    #         # Create a list of Blog objects from the cached data
    #         posts = [Blog(**item) for item in posts]
    #         # Use the Django model manager to create a queryset from the list
    #         return Blog.objects.filter(id__in=[post.id for post in posts])  # noqa

    @swagger_auto_schema(operation_id='listBlog', tags=['Blog'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()  # noqa
    serializer_class = serializers.BlogDetailSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'blog_post_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'blog_post_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Blog(**obj)  # Convert cached data back to Blog object
            return obj

    @swagger_auto_schema(operation_id='retrieveBlog', tags=['Blog'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()  # noqa
    serializer_class = BlogCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(operation_id='createBlog', tags=['Blog'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new post is created
            cache.delete('blog_posts')
        return response


class BlogUpdateAPIView(generics.UpdateAPIView):
    queryset = Blog.objects.all()  # noqa
    serializer_class = serializers.BlogUpdateSerializer
    permission_classes = (IsAuthor,)

    @swagger_auto_schema(operation_id='updateBlog', tags=['Blog'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a post is updated
            cache.delete('blog_posts')
            pk = kwargs.get('pk')
            cache.delete(f'blog_post_{pk}')
        return response

    @swagger_auto_schema(operation_id='updateBlog', tags=['Blog'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a post is updated
            cache.delete('blog_posts')
            pk = kwargs.get('pk')
            cache.delete(f'blog_post_{pk}')
        return response


class BlogDeleteAPIView(generics.DestroyAPIView):
    queryset = Blog.objects.all()  # noqa
    serializer_class = serializers.BlogDetailSerializer
    permission_classes = (IsAuthor,)

    @swagger_auto_schema(
        operation_id='deleteBlog',
        tags=['Blog'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a post is deleted
        cache.delete('blog_posts')
        cache.delete(f'blog_post_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryBlogSerializer
    search_fields = ['name']

    def get_queryset(self):
        categories = cache.get('blog_categories')
        ic(categories)
        if categories is None:
            categories = Category.objects.all()  # noqa
            serializer = self.serializer_class(categories, many=True)
            cache.set('blog_categories', serializer.data)  # Store serialized data in cache
            return categories
        else:
            # Create a list of Category objects from the cached data
            categories = [Category(**item) for item in categories]
            # Use the Django model manager to create a queryset from the list
            return Category.objects.filter(id__in=[category.id for category in categories])  # noqa

    @swagger_auto_schema(operation_id='listCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryBlogSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'blog_category_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'blog_category_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Category(**obj)  # Convert cached data back to Category object
            return obj

    @swagger_auto_schema(operation_id='retrieveCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryBlogCreateSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='createCategory', tags=['Category'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new category is created
            cache.delete('blog_categories')
        return response


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryBlogUpdateSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='updateCategory', tags=['Category'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('blog_categories')
            pk = kwargs.get('pk')
            cache.delete(f'blog_category_{pk}')
        return response

    @swagger_auto_schema(operation_id='updateCategory', tags=['Category'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('blog_categories')
            pk = kwargs.get('pk')
            cache.delete(f'blog_category_{pk}')
        return response


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryBlogSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='deleteCategory', tags=['Category'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a category is deleted
        cache.delete('blog_categories')
        cache.delete(f'blog_category_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)