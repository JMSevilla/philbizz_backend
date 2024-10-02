from philbizz_api.models import Menu, Accounts
from philbizz_api.serializers import MenuSerializer
from rest_framework.response import Response
from rest_framework import status

class MenuRepository:
    @staticmethod
    def create_menu(data_list):
        created_menus = []
        errors = []
        for data in data_list:
            menu_serializer = MenuSerializer(data=data)
            if menu_serializer.is_valid():
                menu_serializer.save()
                created_menus.append(menu_serializer.data)
            else:
                errors.append({"error" : menu_serializer.errors, "data": data})
        if errors:
            return Response({"created_menus": created_menus, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(created_menus, status=status.HTTP_201_CREATED)

    @staticmethod
    def update_menus(data):
        updated_menus = []
        errors = []

        for menu_data in data:
            menu_id = menu_data.get('id')

            try:
                menu_instance = Menu.objects.get(id=menu_id)
            except Menu.DoesNotExist:
                errors.append({"id": menu_id, "error": "Menu not found."})
                continue

            menu_serializer = MenuSerializer(menu_instance, data=menu_data, partial=True)
            if menu_serializer.is_valid():
                menu_serializer.save()
                updated_menus.append(menu_serializer.data)
            else:
                errors.append({"id": menu_id, "errors": menu_serializer.errors})

        if errors:
            return Response({"updated_menus": updated_menus, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"updated_menus": updated_menus}, status=status.HTTP_200_OK)

    @staticmethod
    def get_menus():
        menus = Menu.objects.filter(parent=None)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)