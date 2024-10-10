from django.conf import settings
from django.db import models
import uuid
from enum import Enum
from ckeditor.fields import RichTextField



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

class Menu(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = "pb_menu"

class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Accounts, related_name='liked_blogs', blank=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table = "pb_blog"
        ordering = ['-created_at']

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.blog}"

    class Meta:
        db_table = "pb_comment"