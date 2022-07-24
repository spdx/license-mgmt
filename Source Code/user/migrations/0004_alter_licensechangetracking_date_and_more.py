# Generated by Django 4.0.5 on 2022-06-21 13:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_licenseid_licensechangetracking_license_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensechangetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 19, 20, 31, 674997)),
        ),
        migrations.AlterField(
            model_name='licensechangetracking',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.licensedata'),
        ),
    ]
