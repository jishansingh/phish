# Generated by Django 2.2.4 on 2019-08-18 06:28

from django.db import migrations
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20190817_1129'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='website',
            managers=[
                ('objects', website.models.DomainManager()),
            ],
        ),
    ]