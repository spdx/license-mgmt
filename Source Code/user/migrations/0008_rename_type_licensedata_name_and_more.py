# Generated by Django 4.0.5 on 2022-06-28 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_licensetracking_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='licensedata',
            old_name='type',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 28, 19, 36, 3, 668529)),
        ),
    ]