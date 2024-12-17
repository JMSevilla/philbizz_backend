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
            parent_data = {key: data[key] for key in data if key !='children'}
            parent_serializer = MenuSerializer(data=parent_data)
            if parent_serializer.is_valid():
                parent_instance = parent_serializer.save()
                created_menus.append(parent_serializer.data)

                if 'children' in data:
                    for child_data in data['children']:
                        child_data['parent'] = parent_instance.id
                        child_serializer = MenuSerializer(data=child_data)

                        if child_serializer.is_valid():
                            child_serializer.save()
                            created_menus.append(child_serializer.data)
                        else:
                            errors.append({"error:": child_serializer.errors, "data": child_data})
            else:
                errors.append({"error" : parent_serializer.errors, "data": data})
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

            parent_serializer = MenuSerializer(menu_instance, data=menu_data, partial=True)
            if parent_serializer.is_valid():
                parent_serializer.save()
                updated_menus.append(parent_serializer.data)

                if 'children' in menu_data:
                    for child_data in menu_data['children']:
                        child_id = child_data.get('id')

                        if child_id:
                            try:
                                child_instance = Menu.objects.get(id=child_id)
                            except Menu.DoesNotExist:
                                errors.append({"parent_id": menu_id, "child_id": child_id, "error": "Child menu not found."})
                                continue

                            child_serializer = MenuSerializer(child_instance,data=child_data, partial=True)
                            if child_serializer.is_valid():
                                child_serializer.save()
                                updated_menus.append(child_serializer.data)
                            else:
                                errors.append({"parent_id": menu_id, "child_id": child_id, "errors": child_serializer.errors})
                        else:
                            child_data['parent'] = menu_instance.id
                            child_serializer = MenuSerializer(data=child_data)
                            if child_serializer.is_valid():
                                child_serializer.save()
                                updated_menus.append(child_serializer.data)
                            else:
                                errors.append({"parent_id": menu_id, "child_data": child_data, "errors": child_serializer.errors})

            else:
                errors.append({"id": menu_id, "errors": parent_serializer.errors})

        if errors:
            return Response({"updated_menus": updated_menus, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"updated_menus": updated_menus}, status=status.HTTP_200_OK)
    
    @staticmethod
    def delete_menus(menu_id):
        try:
            parent_menu = Menu.objects.filter(id=menu_id)

            if not parent_menu:
                return Response({"error":"Menu Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            
            child_menu = Menu.objects.filter(parent=parent_menu)
            
            if child_menu.exists():
                delete_child_count = child_menu.count()
                child_menu.delete()
                parent_menu.delete()
                return Response({"message":f"Menus Delete including its child menus {delete_child_count}"}, status=status.HTTP_200_OK)
            
            parent_title  = parent_menu.title
            parent_menu.delete()
            return Response({"message":f"Menu {parent_title} deleted successfully!"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error":str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_menus():
        menus = Menu.objects.filter(parent=None)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)