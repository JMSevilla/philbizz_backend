from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from philbizz_api.services.repository.content_repository import ContentRepository
from philbizz_api.serializers import BusinessSerializer, CardSettingsSerializer, CardInfoSerializer, CardImageSerializer, CardSocialSerializer

class CMSView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            treeview = request.data.get('Treeview')
            textline = request.data.get('Textline')
            texteditor = request.data.get('Texteditor')
            personInvolve = request.data.get("Personnel")

            business = ContentRepository.get_business_by_header(treeview['name'])
            if not business:
                return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)

            ContentRepository.create_card_settings(
                business_id=business.id,
                location=treeview['child'],
                title=textline['required']['title'],
                images=treeview['imageTitle'],
                description=textline['required']['address']
            )

            card = ContentRepository.get_card_settings_by_location_and_title(
                location=treeview['child'],
                title=textline['required']['title']
            )

            if not card:
                return Response({"error": "Card setting not found"}, status=status.HTTP_404_NOT_FOUND)

            card_info = ContentRepository.create_card_info(
                card_id=card.id,
                name=textline['required']['title'],
                contact=textline['required']['contact'],
                email=textline['required']['email'],
                desc=textline['required']['description'],
                content=texteditor,
                servicetype=textline['required']['service'],
                icon_image=textline['required']['image'],
                location_image=textline['required']['location']
            )
            
            if personInvolve and isinstance(personInvolve.get('entries'), list) and personInvolve['entries']:
                for key in personInvolve['entries']:
                    if isinstance(key, dict):
                        name = key.get('personnelName')
                        position = key.get('position')
                        image = key.get('imagePreview')

                        if name: 
                            ContentRepository.create_card_person(info_id=card_info.id, name=name, position=position, image=image)

           
            if 'option' in textline and len(textline['option']) > 0:
                for item in textline['option']:
                    if isinstance(item, dict):
                        value = item.get('value')
                        if value: 
                            ContentRepository.create_card_image(info_id=card_info.id, image_url=value)

            
            if 'social' in textline:
                for item in textline['social']:
                    if isinstance(item, dict):
                        social = item.get('social')
                        link = item.get('link')
                        if link:  
                            ContentRepository.create_card_social(info_id=card_info.id, social_media=social, social_value=link)


            return Response({"message": f"New {treeview['name']} card created!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CSMUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            treeview = request.data.get('Treeview')
            textline = request.data.get('Textline')
            texteditor = request.data.get('Texteditor')
            personInvolve = request.data.get("Personnel")
            
            if not treeview or not textline or not texteditor:
                return Response({"error": "Invalid or incomplete data"}, status=status.HTTP_400_BAD_REQUEST)

            business = ContentRepository.get_business_by_header(treeview.get('name'))
            if not business:
                return Response({"error": "Business not found"}, status=status.HTTP_404_NOT_FOUND)

            ContentRepository.update_card_settings(
                id=treeview.get('uuid'),
                location=treeview.get('child'),
                title=textline['required'].get('title'),
                images=treeview.get('imageTitle'),
                description=textline['required'].get('address')
            )

            card_info = ContentRepository.update_card_info(
                id=textline['required'].get('uuid'),
                name=textline['required'].get('title'),
                contact=textline['required'].get('contact'),
                email=textline['required'].get('email'),
                desc=textline['required'].get('description'),
                content=texteditor,
                servicetype=textline['required'].get('service'),
                icon_image=textline['required'].get('image'),
                location_image=textline['required'].get('location')
            )

            if personInvolve and 'entries' in personInvolve:
                for key in personInvolve['entries']:
                    if len(key) > 0:
                        if isinstance(key, dict):
                            id = key.get('uuid')
                            name = key.get('personnelName')
                            position = key.get('position')
                            image = key.get('imagePreview')
                            if id is None:
                                ContentRepository.create_card_person(info_id=card_info.id, name=name, position=position, image=image)
                            else:
                                ContentRepository.update_person_involve(id=id, name=name, position=position, image=image)
                        else:
                            return Response({"error": "Invalid item in 'person details'"}, status=status.HTTP_400_BAD_REQUEST)

            
            if 'option' in textline and isinstance(textline['option'], list):
                for option in textline['option']:
                    if isinstance(option, dict):
                        id = option.get('uuid')
                        image_url = option.get('value')
                        if id is None:
                            ContentRepository.create_card_image(info_id=card_info.id, image_url=image_url)
                        else:
                            ContentRepository.update_card_image_link(id=id, image_url=image_url)
                    else:
                        return Response({"error": "Invalid item in 'image_link'"}, status=status.HTTP_400_BAD_REQUEST)

            
            if 'social' in textline:
                for key in textline['social']:
                    if isinstance(key, dict):
                        id = key.get('uuid')
                        media = key.get('social')
                        value = key.get('link')
                        if id is None:
                            ContentRepository.create_card_social(info_id=card_info.id, social_media=media, social_value=value)
                        else:
                            ContentRepository.update_card_social(id=id, social_media=media, social_value=value)
                    else:
                        return Response({"error": "Invalid item in 'social'"}, status=status.HTTP_400_BAD_REQUEST)
                        
            return Response({"message": f"Update {treeview.get('name')} card successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class CMSViewList(APIView) :
    permission_classes = []
    def get(self, request):
        header = request.query_params.get('header',None)
        search = request.query_params.get('search', None)
        item_pages = 15
        if not header:
            return Response({"error": "Header parameter is required."}, status=400)
        content_list = ContentRepository.view_content_list()
        filtered_content = [
            item for item in content_list if item['business']['header'] == header
        ]
      
        if search:
            filtered_content = [
                item for item in filtered_content
                if search.lower() in item.get('title', '').lower() or
                search.lower() in item.get('description', '').lower()
            ]
        
        paginator = PageNumberPagination()
        paginator.page_size = item_pages
        paginated_content = paginator.paginate_queryset(filtered_content, request)

        if filtered_content:
            return paginator.get_paginated_response(paginated_content)
        else:
            return Response({"message": "No content found for the specified header."}, status=404)
        
class CMSContentViewInfo(APIView) :
    permission_classes = []
    def get(self, request):
        content_id = request.query_params.get('content', None)
        content_view = ContentRepository.view_content(id=content_id)
        return Response(content_view)

class CMSMainContentList(APIView):
    permission_classes = []
    def get(self, request):
        main_content_list = ContentRepository.main_content_list()
        return Response(main_content_list)


