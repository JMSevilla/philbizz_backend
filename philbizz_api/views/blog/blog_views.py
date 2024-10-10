from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from philbizz_api.services.repository.blog_repository import BlogRepository

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return BlogRepository.create_blog(data=request.data)

    def get(self, request):
        return BlogRepository.get_all_blogs()

class BlogLikeView(APIView):

    def post(self, request, blog_id):
        return BlogRepository.like_blog(blog_id=blog_id)

    def get(self, request, blog_id):
        count = BlogRepository.get_likes_count(blog_id)
        return Response({"likes": count}, status=status.HTTP_200_OK)

class CommentView(APIView):

    def post(self, request, blog_id):
        data = request.data.copy()
        data['blog'] = blog_id
        return BlogRepository.create_comment(data, request.user)

    def get(self, request, blog_id):
        return BlogRepository.get_blog_comment(blog_id)