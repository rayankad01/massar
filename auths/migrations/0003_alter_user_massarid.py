# Generated by Django 4.2.13 on 2024-06-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_rename_massar_id_user_massarid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='massarID',
            field=models.EmailField(max_length=254),
        ),
    ]