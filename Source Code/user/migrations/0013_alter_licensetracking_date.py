# Generated by Django 4.0.5 on 2022-07-03 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_namespace_alter_licensedata_identifier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 21, 40, 52, 132760)),
        ),
    ]
