import uuid
from datetime import timedelta
from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate
from philbizz_api.models import Accounts, Credentials, TokenizeInformation, AccessGroup, AccountStatus
from philbizz_api.services.utils import hash_password, verify_password, AccountLoginResponse, ResponseCode, \
    create_token, generate_refresh_token, AccessInformation
from django.utils import timezone
from django.db import transaction
from philbizz_api.services.validations.accounts.validation import AccountValidationService
from uuid import UUID
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
class InternalLinkedGuids:
    def __init__(self, credentials_id, tokenize_information_id, access_group_id, internal_account_id):
        self.credentials_id = credentials_id
        self.tokenize_information_id = tokenize_information_id
        self.access_group_id = access_group_id
        self.internal_account_id = internal_account_id

    def to_dict(self):
        return {
            'CredentialsId': self.credentials_id,
            'TokenizeInformationId': self.tokenize_information_id,
            'AccessGroupId': self.access_group_id,
            'InternalAccountId': self.internal_account_id
        }

class MultiInternalDataTypes:
    def __init__(self, credentials, tokenize_information, access_group, account_id):
        self.credentials = credentials
        self.tokenize_information = tokenize_information
        self.access_group = access_group
        self.account_id = account_id

    def to_dict(self):
        return {
            'Credentials': self.credentials,
            'TokenizeInformation': self.tokenize_information,
            'AccessGroup': self.access_group,
            'AccountId': self.account_id
        }
class AccountRepository:

    @staticmethod
    @transaction.atomic
    def internal_key_accounts(data) -> ResponseCode:
        try:
            if User.objects.filter(email=data['email']).exists():
                return ResponseCode.InternalAccountExists.value

            access_user = User(
                email=data['email'],
                username=data['email']
            )
            access_user.set_password(data['password'])
            access_user.save()
            return ResponseCode.Success.value
        except Exception as e:
            return ResponseCode.InternalServerError.value

    @staticmethod
    @transaction.atomic
    def internal_access_creation(data) -> ResponseCode:
        try:
            if Credentials.objects.filter(email=data['email']).exists() or TokenizeInformation.objects.filter(
                    email=data['email']).exists():
                return ResponseCode.InternalAccountExists.value
            code = AccountRepository.internal_key_accounts(data)
            if code == ResponseCode.Success.value:
                AccountRepository.account_creation(data)
            return ResponseCode.Success.value
        except Exception as e:
            return ResponseCode.InternalServerError.value
    @staticmethod
    @transaction.atomic
    def account_creation(data) -> ResponseCode:
        try:

            tokenize_info_data = {
                'firstname': data['firstname'],
                'middlename': data.get('middlename', ''),
                'lastname': data['lastname'],
                'email': data['email'],
                'mobile_number': data.get('mobile_number', ''),
                'imgurl': data.get('imgurl', '')
            }

            AccountValidationService.validate_account_data(data)

            hashed_password = hash_password(data['password'])

            tokenize_info = TokenizeInformation.objects.create(**tokenize_info_data)

            credentials = Credentials.objects.create(
                email=data['email'],
                password=hashed_password
            )

            access_group = AccessGroup.objects.create(access_level=data['access_level'])

            Accounts.objects.create(
                credentials=credentials,
                tokenize_information=tokenize_info,
                access_group=access_group,
                account_status_enum=AccountStatus.ACTIVE,
                updated_at=timezone.now(),
                created_at=timezone.now()
            )

            return ResponseCode.Success
        except Exception as e:
            return ResponseCode.InternalServerError

    @staticmethod
    @transaction.atomic
    def security_linked(email, password) -> AccessInformation:
        try:
            account = authenticate(username=email, password=password)
            if account is None:
                raise AuthenticationFailed("Unauthorized Access - Invalid credentials")

            roles = account.groups.values_list('name', flat=True)

            if not roles:
                roles = ['default_role']

            claims = {
                'username': account.username,
                'jti': str(uuid.uuid4()),
                'roles': list(roles)
            }

            refresh = RefreshToken.for_user(account)
            access_token = str(refresh.access_token)

            account.refresh_token = str(refresh)
            account.refresh_token_expiry_time = timezone.now() + timedelta(
                days=settings.JWT_REFRESH_TOKEN_VALIDITY_IN_DAYS)
            account.save()

            return AccessInformation(
                access_token=access_token,
                refresh_token=str(refresh),
                expiration=refresh.access_token.payload.get('exp'),
            )

        except Exception as e:
            raise AuthenticationFailed(f"Unauthorized Access: {str(e)}")
    @staticmethod
    @transaction.atomic
    def account_login(data: object) -> Union[AccountLoginResponse, ResponseCode]:
        try:
            AccountValidationService.validate_account_login(data)
            process_result = AccountRepository.multi_internal_models_extract_by_email(data.get('email'))

            verify = verify_password(data.get('password'), process_result.credentials.password)
            if verify:
                payload = {
                    'email': data.get('email'),
                    'password': data.get('password')
                }
                accessInformation = AccountRepository.security_linked(**payload)
                return AccountLoginResponse(
                    access_token_response=AccessInformation(
                        access_token=accessInformation.access_token,
                        refresh_token=accessInformation.refresh_token,
                        expiration=accessInformation.expiration
                    ),
                    response_code=ResponseCode.Success.value,
                    account_id=process_result.account_id,
                    access_level=process_result.access_group.access_level,
                    is_2fa_enabled=False
                )
            else:
                return ResponseCode.Unauthorized
        except Exception as e:
            return ResponseCode.Unauthorized
    @transaction.atomic
    def internal_credentials_extract_guid_by_email(email: str) -> UUID:
        try:
            credentials_id = Credentials.objects.filter(email=email).values_list('id', flat=True).first()
            internal_account_id = Accounts.objects.filter(credentials_id=credentials_id).values_list('id', flat=True).first()

            if not internal_account_id:
                raise ValueError("Internal Account ID is null or empty")
            if not credentials_id:
                raise ValueError("Credentials ID is null or empty")

            return internal_account_id
        except ObjectDoesNotExist:
            raise ValueError("No matching records found for the given username")

    def get_internal_linked_ids_by_email(email: str) -> InternalLinkedGuids:
        internal_id = AccountRepository.internal_credentials_extract_guid_by_email(email)

        linked_ids = Accounts.objects.filter(id=internal_id).values(
            'credentials_id', 'tokenize_information_id', 'access_group_id'
        ).first()

        if not linked_ids:
            raise ValueError("No linked IDs found for the given internal account ID")

        return InternalLinkedGuids(
            credentials_id=linked_ids['credentials_id'],
            tokenize_information_id=linked_ids['tokenize_information_id'],
            access_group_id=linked_ids['access_group_id'],
            internal_account_id=internal_id
        )

    def multi_internal_models_extract_by_email(email: str) -> MultiInternalDataTypes:
        internal_ids = AccountRepository.get_internal_linked_ids_by_email(email)

        credentials_task = Credentials.objects.get(id=internal_ids.credentials_id)
        tokenize_task = TokenizeInformation.objects.get(id=internal_ids.tokenize_information_id)
        access_group_task = AccessGroup.objects.get(id=internal_ids.access_group_id)

        if not credentials_task or not tokenize_task or not access_group_task:
            raise ValueError("One or more required entities were not found.")

        return MultiInternalDataTypes(
            credentials=credentials_task,
            tokenize_information=tokenize_task,
            access_group=access_group_task,
            account_id=internal_ids.internal_account_id
        )