# Generated by Django 2.2.4 on 2019-08-17 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='password',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='page',
            name='username',
            field=models.IntegerField(default=0),
        ),
    ]