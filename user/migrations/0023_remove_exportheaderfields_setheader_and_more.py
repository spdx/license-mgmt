# Generated by Django 4.0.5 on 2022-08-23 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_alter_exportheaderfields_creationinfocreated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exportheaderfields',
            name='setHeader',
        ),
        migrations.AlterField(
            model_name='exportheaderfields',
            name='creationInfoCreated',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 12, 32, 28, 120323)),
        ),
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 12, 32, 28, 120323)),
        ),
    ]
