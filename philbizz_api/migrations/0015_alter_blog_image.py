# Generated by Django 5.1.1 on 2024-11-19 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('philbizz_api', '0014_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blogs/'),
        ),
    ]
