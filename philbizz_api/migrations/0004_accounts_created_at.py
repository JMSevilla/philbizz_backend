# Generated by Django 5.1.1 on 2024-09-23 16:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('philbizz_api', '0003_accounts_updated_at_alter_accessgroup_access_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
