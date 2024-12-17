from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from philbizz_api.services.repository.navbar_repository import NavbarRepository

class NavbarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return NavbarRepository.create_navbar(request.data)
    
    def put(self, request):
        return NavbarRepository.update_navbar(request.data)
    def delete(self, request):
        navbar_id = request.query_params.get("navbar")
        return NavbarRepository.delete_navbar(nabvar_id=navbar_id)

class NavbarListView(APIView):
    permission_classes = []
    def get(self, request):
        return NavbarRepository.get_navbar()