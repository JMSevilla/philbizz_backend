# Generated by Django 5.1.1 on 2024-10-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('philbizz_api', '0005_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_blogs', to='philbizz_api.accounts'),
        ),
    ]
