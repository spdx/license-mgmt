# Generated by Django 4.0.5 on 2022-06-17 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_licensechangetracking_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='licensechangetracking',
            old_name='licenseId',
            new_name='license',
        ),
        migrations.AlterField(
            model_name='licensechangetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 12, 14, 9, 178800)),
        ),
    ]