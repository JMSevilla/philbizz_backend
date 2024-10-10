from rest_framework import serializers
from philbizz_api.models import AccountStatus, AccessLevel, TokenizeInformation, Menu, Blog, Comment
from philbizz_api.services.repository.account_repository import AccountRepository
from philbizz_api.services.repository.auth_repository import ValidateTokenizeCommand, AuthRepository
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

class ValidateTokenizeSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
    account_id = serializers.UUIDField()

    def validate(self, attrs):
        return attrs

    def validate_token(self, validated_data):
        command = ValidateTokenizeCommand(**validated_data)
        result = AuthRepository.validate_tokenize_information(command)
        return result

class TokenizeInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenizeInformation
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'path', 'parent', 'children']

    def get_children(self, obj):
        return MenuSerializer(obj.children.all(), many=True).data

    def validate_path(self, value):
        if not value.startswith('/'):
            raise serializers.ValidationError("Path must start with a '/' character.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'image', 'content', 'created_at', 'updated_at']
