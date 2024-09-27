from philbizz_api.models import Menu, Accounts
from philbizz_api.serializers import MenuSerializer
from rest_framework.response import Response
from rest_framework import status

class MenuRepository:
    @staticmethod
    def create_menu(data):
        menu_serializer = MenuSerializer(data=data)
        if menu_serializer.is_valid():
            menu_serializer.save()
            return Response(menu_serializer.data, status=status.HTTP_201_CREATED)
        return Response(menu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_menus():
        menus = Menu.objects.filter(parent=None)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)