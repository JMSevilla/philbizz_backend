from django.db import models
import uuid
from enum import Enum

class AccessLevel(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    CUSTOMER = 'CUSTOMER', 'Customer'
class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class AccessGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    access_level = models.CharField(
        max_length=50,
        choices=AccessLevel.choices,
        default=AccessLevel.CUSTOMER
    )

    class Meta:
        db_table = "pb_access_group"

class TokenizeInformation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255)
    email = models.EmailField()
    imgurl = models.URLField(blank=True, null=True)
    mobile_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        db_table = "pb_tokenize_information"

class Credentials(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "pb_credentials"

class Accounts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    credentials = models.OneToOneField(Credentials, on_delete=models.CASCADE)
    tokenize_information = models.OneToOneField(TokenizeInformation, on_delete=models.CASCADE)
    access_group = models.ForeignKey(AccessGroup, on_delete=models.SET_NULL, null=True)
    account_status_enum = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in AccountStatus],
        default=AccountStatus.ACTIVE.name,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pb_accounts"
        
class BlackListedTokens(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pb_blacklisted_tokens"