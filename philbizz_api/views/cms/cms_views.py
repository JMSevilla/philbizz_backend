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

            for key in personInvolve['entries']:
                name = key['personnelName']
                position = key['position']
                image = key['imagePreview']
                ContentRepository.create_card_person(info_id=card_info.id, name=name, position=position, image=image)

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