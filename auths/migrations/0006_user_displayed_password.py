# Generated by Django 4.2.13 on 2024-06-16 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0005_user_classe'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='displayed_password',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
