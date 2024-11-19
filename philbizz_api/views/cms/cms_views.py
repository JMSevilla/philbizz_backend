from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
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
            if 'entries' in personInvolve and len(personInvolve['entries']) > 0:
                for key in personInvolve['entries']:
                    if len(key) > 0 : 
                        name = key['personnelName']
                        position = key['position']
                        image = key['imagePreview']
                        ContentRepository.create_card_person(info_id=card_info.id, name=name, position=position, image=image)
            
            if 'option' in textline and len(textline['option']) > 0 :
                for key in textline['option']:
                    value = textline['option'][key]['value']
                    ContentRepository.create_card_image(info_id=card_info.id, image_url=value)

            for item in textline['social']:
                social = item['social']
                link = item['link']
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
        
class CSMViewList(APIView) :
    permission_classes = []
    def get(self, request):
        content_list = ContentRepository.view_content()
        return Response(content_list)

