# Generated by Django 4.0.5 on 2022-08-17 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_exportheaderfields_creationinfocreated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportheaderfields',
            name='creationInfoCreated',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 17, 22, 22, 48, 437774)),
        ),
        migrations.AlterField(
            model_name='exportheaderfields',
            name='creationInfoCreatorsOrganization',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='exportheaderfields',
            name='creationInfoCreatorsPerson',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='exportheaderfields',
            name='creationInfoCreatorsTools',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 17, 22, 22, 48, 437774)),
        ),
    ]
