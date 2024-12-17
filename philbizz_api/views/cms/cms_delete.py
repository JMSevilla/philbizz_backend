from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from philbizz_api.services.repository.content_repository import ContentRepository

class CMSDeleteContent(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        try:
            content_id = request.data.get('content')
            if not content_id:
                return Response({"error":"Content ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            result = ContentRepository.delete_content(content_id=content_id)

            if "erro" in result:
                return Response({"error",result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message":result['message']}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    