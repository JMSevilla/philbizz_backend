from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from philbizz_api.services.repository.menu_repository import MenuRepository



class MenuView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return MenuRepository.create_menu(request.data)

    def put(self, request):
        return MenuRepository.update_menus(request.data)
    
    def delete(self, request):
        menu_id= request.query_params.get("treeviewID")
        return MenuRepository.delete_menus(menu_id=menu_id)

        

class MenuListView(APIView):
    permission_classes = []
    def get(self, request):
        return MenuRepository.get_menus()

