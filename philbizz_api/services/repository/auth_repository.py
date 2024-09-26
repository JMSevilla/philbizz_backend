from typing import Optional
from uuid import UUID
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from philbizz_api.models import BlackListedTokens, TokenizeInformation, Accounts
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.conf import settings

class ValidateTokenizeCommand:
    def __init__(self, access_token: str, account_id: UUID):
        self.access_token = access_token
        self.account_id = account_id

class TokenizeInformationResponse:
    def __init__(self, tokenize_information: Optional[TokenizeInformation] = None):
        self.tokenize_information = tokenize_information
class AuthRepository:
    @staticmethod
    def black_list_tokens(token: str):
        if not token:
            raise ValidationError("Token is required.")
        blacklisted_token = BlackListedTokens(
            token=token,
            blacklisted_at=timezone.now()
        )
        blacklisted_token.save()

    @staticmethod
    def is_token_blacklisted(token: str) -> bool:
        return BlackListedTokens.objects.filter(token=token).exists()

    @staticmethod
    @transaction.atomic
    def validate_tokenize_information(data: ValidateTokenizeCommand) -> TokenizeInformationResponse:
        token_response = TokenizeInformationResponse()
        key = settings.JWT_SECRET_KEY.encode('utf-8')

        try:
            if AuthRepository.is_token_blacklisted(data.access_token):
                return token_response

            decoded_token = jwt.decode(data.access_token, key, algorithms=["HS256"])  # Use this decoded_token to create another validation from the models.

            get_internal_account: Accounts = Accounts.objects.filter(id=data.account_id).get()
            if get_internal_account is None:
                return token_response

            get_internal_tokenize_information: TokenizeInformation = TokenizeInformation.objects.filter(
                id=get_internal_account.tokenize_information_id).get()
            if get_internal_tokenize_information is None:
                return token_response

            return TokenizeInformationResponse(tokenize_information=get_internal_tokenize_information)

        except (ExpiredSignatureError, InvalidTokenError, jwt.PyJWTError) as e:
            return TokenizeInformationResponse()
        except Exception as e:
            return TokenizeInformationResponse()