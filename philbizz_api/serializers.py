from rest_framework import serializers
from philbizz_api.models import AccountStatus, AccessLevel
from philbizz_api.services.repository.account_repository import AccountRepository
from philbizz_api.services.utils import ResponseCode


class AccountCreateSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=255)
    middlename = serializers.CharField(max_length=255, allow_blank=True, required=False)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=12, allow_blank=True, required=False)
    imgurl = serializers.URLField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    access_level = serializers.ChoiceField(choices=AccessLevel.choices, default=AccessLevel.CUSTOMER)
    account_status_enum = serializers.ChoiceField(choices=[(status.name, status.value) for status in AccountStatus],
                                                  default=AccountStatus.ACTIVE.name)

    def create(self, validated_data):
        return AccountRepository.internal_access_creation(validated_data)

class AccountLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        process_result = AccountRepository.account_login(validated_data)
        if isinstance(process_result, ResponseCode):
            if process_result == ResponseCode.Unauthorized:
                raise serializers.ValidationError({'detail': "Invalid credentials."})
        return process_result