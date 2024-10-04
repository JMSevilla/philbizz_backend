from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from philbizz_api.services.repository.blog_repository import BlogRepository

class BlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return BlogRepository.create_blog(data=request.data)

    def get(self, request):
        return BlogRepository.get_all_blogs()