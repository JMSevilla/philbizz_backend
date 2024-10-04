from philbizz_api.models import Blog
from philbizz_api.serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework import status

class BlogRepository:
    @staticmethod
    def create_blog(data) -> Response:
        blog_serializer = BlogSerializer(data=data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response(blog_serializer.data, status=status.HTTP_201_CREATED)
        return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_all_blogs():
        blogs = Blog.objects.all().order_by('-created_at')
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data, status=status.HTTP_200_OK)