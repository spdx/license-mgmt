# Generated by Django 4.0.5 on 2022-07-04 08:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_licensetracking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 4, 13, 52, 56, 856727)),
        ),
    ]
