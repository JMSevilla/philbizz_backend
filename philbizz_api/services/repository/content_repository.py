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
    def update_card_settings(id,location, title, images, description):
        try:
            card_settings = CardSettings.objects.get(id=id)
            card_settings.location = location
            card_settings.title = title
            card_settings.images = images
            card_settings.description = description

            card_settings.save()
            return card_settings
        except CardSettings.DoesNotExist:
            return None
    @staticmethod
    def update_card_info(id, name=None, contact=None, email=None, desc=None, content=None, servicetype=None, icon_image=None, location_image=None):
        try: 
            card_info = CardInfo.objects.get(id=id)
            if name is not None:
                card_info.name = name
            if contact is not None:
                card_info.contact = contact
            if email is not None:
                card_info.email = email
            if desc is not None:
                card_info.desc = desc
            if content is not None:
                card_info.content = content
            if servicetype is not None:
                card_info.servicetype = servicetype
            if icon_image is not None:
                card_info.icon_image = icon_image
            if location_image is not None:
                card_info.location_image = location_image

            card_info.save()
            return card_info
        except CardInfo.DoesNotExist:
            return None
        
    @staticmethod
    def update_person_involve(id, name=None, position=None, image=None):
        try:
            person_involve = PersonInvolve.objects.get(id=id)
            if name is not None:
                person_involve.name = name
            if position is not None:
                person_involve.position = position
            if image is not None:
                person_involve.image = image

            person_involve.save()
            return person_involve
        except PersonInvolve.DoesNotExist:
            return None

    @staticmethod
    def update_card_social(id, social_media=None, social_value=None):
        try:
            card_social = CardSocial.objects.get(id=id)

            if social_media is not None:
                card_social.social_media = social_media
            if social_value is not None:
                card_social.social_value = social_value

            card_social.save()
            return card_social
        except CardSocial.DoesNotExist:
            return None
        
    @staticmethod
    def update_card_image_link(id,image_url=None):
        try:
            card_image_link = CardImage.objects.get(id=id)
            if image_url is not None:
                card_image_link.image_url = image_url

            card_image_link.save()
            return card_image_link
        except CardImage.DoesNotExist:
            return None

    @staticmethod
    def view_content_list():

        content_list = []

        card_setting = CardSettings.objects.all()
        
        for card in card_setting :
            business = card.business if card.business else None
            business_info = {
                'id': business.navbar_id if business else None,
                'header': business.header if business else None,
            }
            card_info = CardInfo.objects.filter(card=card)
            for info in card_info:
                description = info.desc


            content_list.append({
                'id': card.id,
                'business': business_info,
                'location': card.location,
                'title': card.title,
                'address': card.description,
                'title_image': card.images,
                'description': description
            })
        
        return content_list
    
    def view_content(id):
        content_view = []
        card_info = CardInfo.objects.filter(card = id)
        
        for info in card_info:
            people = PersonInvolve.objects.filter(card=info)
            people_list = [{
                'id': person.id,
                'name': person.name,
                'position': person.position,
                'image': person.image
                } for person in people]
            
            social_link = CardSocial.objects.filter(card=info)
            social_link_list = [{
                'id': social.id,
                'social_media': social.social_media,
                'social_value': social.social_value
            } for social in social_link]

            images = CardImage.objects.filter(card=info)
            image_list = [{
                'id': image.id,
                'images': image.image_url
            } for image in images]


            content_view.append({
                'id': info.id,
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

        return content_view
    
    def main_content_list() :

        main_content = []
        
        business_header = Business.objects.all()

        for header in business_header:

            content_list = CardSettings.objects.filter(business = header)[:4]
            header_content = []
            for card in content_list:
                content_info = CardInfo.objects.filter(card=card)
                for info in content_info:
                    description = info.desc

                header_content.append({
                'id': card.id,
                'location': card.location,
                'title': card.title,
                'address': card.description,
                'title_image': card.images,
                'description': description
                })

            main_content.append({
                'title': header.header,
                'list': header_content
            })

        return main_content


