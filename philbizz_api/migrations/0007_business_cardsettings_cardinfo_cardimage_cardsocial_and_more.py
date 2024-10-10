# Generated by Django 5.1.1 on 2024-10-10 11:50

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('philbizz_api', '0006_blog_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pb_business',
            },
        ),
        migrations.CreateModel(
            name='CardSettings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('images', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='philbizz_api.business')),
            ],
            options={
                'db_table': 'pb_cardsettings',
            },
        ),
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('desc', models.TextField()),
                ('content', models.TextField()),
                ('servicetype', models.CharField(max_length=255)),
                ('icon_image', models.TextField(blank=True, null=True)),
                ('location_image', models.TextField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='philbizz_api.cardsettings')),
            ],
            options={
                'db_table': 'pb_cardinfo',
            },
        ),
        migrations.CreateModel(
            name='CardImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_url', models.TextField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='philbizz_api.cardsettings')),
            ],
            options={
                'db_table': 'pb_cardimage',
            },
        ),
        migrations.CreateModel(
            name='CardSocial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('social_media', models.CharField(max_length=255)),
                ('social_value', models.CharField(max_length=255)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='philbizz_api.cardsettings')),
            ],
            options={
                'db_table': 'pb_cardsocial',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='philbizz_api.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pb_comment',
            },
        ),
    ]
