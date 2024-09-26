# Generated by Django 5.1.1 on 2024-09-26 09:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('access_level', models.CharField(choices=[('ADMIN', 'Admin'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=50)),
            ],
            options={
                'db_table': 'pb_access_group',
            },
        ),
        migrations.CreateModel(
            name='BlackListedTokens',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=255)),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pb_blacklisted_tokens',
            },
        ),
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pb_credentials',
            },
        ),
        migrations.CreateModel(
            name='TokenizeInformation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=255)),
                ('middlename', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('imgurl', models.URLField(blank=True, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=12, null=True)),
            ],
            options={
                'db_table': 'pb_tokenize_information',
            },
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_status_enum', models.CharField(choices=[('ACTIVE', 'active'), ('INACTIVE', 'inactive'), ('SUSPENDED', 'suspended')], default='ACTIVE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('access_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='philbizz_api.accessgroup')),
                ('credentials', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='philbizz_api.credentials')),
                ('tokenize_information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='philbizz_api.tokenizeinformation')),
            ],
            options={
                'db_table': 'pb_accounts',
            },
        ),
    ]
