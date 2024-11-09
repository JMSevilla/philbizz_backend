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