from philbizz_api.models import Blog, Comment
from philbizz_api.serializers import BlogSerializer, CommentSerializer
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

    @staticmethod
    def like_blog(blog_id, user) -> Response:
        try:
            blog = Blog.objects.get(id=blog_id)
            if user in blog.likes.all():
                blog.likes.remove(user)
                return Response({"message": "Blog unliked."}, status=status.HTTP_200_OK)
            else:
                blog.likes.add(user)
                return Response({"message": "Blog liked."}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"message": "Blog does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_likes_count(blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
            return blog.likes.count()
        except Blog.DoesNotExist:
            return 0

    @staticmethod
    def create_comment(data, user):
        comment_serializer = CommentSerializer(data=data)
        if comment_serializer.is_valid():
            comment_serializer.save(user=user)
            return Response(data=comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_blog_comment(blog_id):
        comments = Comment.objects.filter(id=blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)