from philbizz_api.models import NavbarContent, Business 
from philbizz_api.serializers import NavbarSerializer, BusinessSerializer
from rest_framework.response import Response
from rest_framework import status

class NavbarRepository:
    @staticmethod
    def create_navbar(data) -> Response:
        navbar_serializer = NavbarSerializer(data=data)
        if navbar_serializer.is_valid():
            navbar_instance = navbar_serializer.save()

            navbar_name_lower = navbar_instance.name
            business_data = {"header": navbar_name_lower, "navbar": navbar_instance.id}
            business_serializer = BusinessSerializer(data=business_data)

            if business_serializer.is_valid():
                business_serializer.save()
            else:
                return Response(business_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(navbar_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(navbar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def update_navbar(data): 
        navID = data.get('id');   
        try:
            navbar_instance = NavbarContent.objects.get(id=navID)
        except NavbarContent.DoesNotExist:
            return Response({"id": navID, "error": "Navbar Not Found."}, status=status.HTTP_404_NOT_FOUND)
            
        navbar_serializer = NavbarSerializer(navbar_instance, data=data, partial=True)
        if navbar_serializer.is_valid():
            updated_navbar = navbar_serializer.save()

            try:
                business_instance = Business.objects.get(navbar=navbar_instance)
                business_instance.header = updated_navbar.name
                business_instance.save()
            except Business.DoesNotExist:
                return Response({"error": "Related Business entry not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(navbar_serializer.data, status=status.HTTP_200_OK)
        
        return Response(navbar_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete_navbar(nabvar_id):
        try:
            navbar_instance = NavbarContent.objects.filter(id=nabvar_id)
            if not navbar_instance:
                return Response({"error":"Navbar Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            
            business = Business.objects.filter(navbar=navbar_instance).first()
            if business:
                business.delete()
                
            nav_name = navbar_instance.name
            navbar_instance.delete()
        
            return Response({"message":f"{nav_name} is successfully deleted!"}, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def get_navbar():
        navbars = NavbarContent.objects.all()
        navbar_serializer = NavbarSerializer(navbars, many=True)
        return Response(navbar_serializer.data, status=status.HTTP_200_OK)