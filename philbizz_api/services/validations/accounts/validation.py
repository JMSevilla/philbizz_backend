from django.core.exceptions import ValidationError
from philbizz_api.models import TokenizeInformation, Credentials

class AccountValidationService:

    @staticmethod
    def validate_account_data(data):
        if Credentials.objects.filter(email=data.get('email')).exists():
            raise ValidationError("An account with this email already exists.")

        if TokenizeInformation.objects.filter(email=data.get('email')).exists():
            raise ValidationError("An account with this email already exists.")

        required_fields = ['firstname', 'lastname', 'email', 'mobile_number']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        return None

    @staticmethod
    def validate_account_login(data):
        if not Credentials.objects.filter(email=data.get('email')).exists():
            raise ValidationError("The account with this email does not exist.")

        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        return None
