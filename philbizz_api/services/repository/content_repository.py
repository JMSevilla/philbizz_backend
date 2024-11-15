from philbizz_api.models import Business, CardSettings, CardInfo, CardImage, CardSocial, PersonInvolve
class ContentRepository:

    @staticmethod
    def get_business_by_header(header):
        try:
            return Business.objects.get(header=header)
        except Business.DoesNotExist:
            return None

    @staticmethod
    def create_card_settings(business_id, location, title, images, description):
        card_setting = CardSettings.objects.create(
            business_id=business_id,
            location=location,
            title=title,
            images=images,
            description=description
        )
        return card_setting

    @staticmethod
    def get_card_settings_by_location_and_title(location, title):
        try:
            return CardSettings.objects.get(location=location, title=title)
        except CardSettings.DoesNotExist:
            return None

    @staticmethod
    def create_card_info(card_id, name, contact, email, desc, content, servicetype, icon_image, location_image):
        return CardInfo.objects.create(
            card_id=card_id,
            name=name,
            contact=contact,
            email=email,
            desc=desc,
            content=content,
            servicetype=servicetype,
            icon_image=icon_image,
            location_image=location_image
        )

    @staticmethod
    def create_card_person(info_id, name, position, image ):
        return PersonInvolve.objects.create(
            card_id = info_id,
            name = name,
            position = position,
            image = image
        )

    @staticmethod
    def create_card_image(info_id, image_url):
        return CardImage.objects.create(card_id=info_id, image_url=image_url)

    @staticmethod
    def create_card_social(info_id, social_media, social_value):
        return CardSocial.objects.create(card_id=info_id, social_media=social_media, social_value=social_value)
    
    @staticmethod
    def view_content():
        content_list = []

        card_setting = CardSettings.objects.all()

        for card in card_setting :
            business = card.business if card.business else None
            business_info = {
                'id': business.navbar_id if business else None,
                'header': business.header if business else None,
            }

            card_info = CardInfo.objects.filter(card = card)
            card_info_list = []
            for info in card_info:
                people = PersonInvolve.objects.filter(card=info)
                people_list = [{
                    'name': person.name,
                    'position': person.position,
                    'image': person.image
                } for person in people]

            social_link = CardSocial.objects.filter(card=info)
            social_link_list = [{
                'social_media': social.social_media,
                'social_value': social.social_value
            } for social in social_link]

            images = CardImage.objects.filter(card=info)
            image_list = [image.image_url for image in images]

            card_info_list.append({
                 'name': info.name,
                    'contact': info.contact,
                    'email': info.email,
                    'desc': info.desc,
                    'content': info.content,
                    'servicetype': info.servicetype,
                    'icon_image': info.icon_image,
                    'location_image': info.location_image,
                    'people_involved': people_list,
                    'social_links': social_link_list,
                    'images': image_list
            })

            content_list.append({
                'business': business_info,
                'location': card.location,
                'title': card.title,
                'description': card.description,
                'card_info': card_info_list
            })
        
        return content_list