# Generated by Django 4.0.5 on 2022-06-22 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_licensetracking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 22, 18, 20, 8, 887715)),
        ),
    ]
