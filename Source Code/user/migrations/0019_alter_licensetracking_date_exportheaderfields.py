# Generated by Django 4.0.5 on 2022-08-17 15:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0018_alter_licensetracking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensetracking',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 17, 21, 16, 22, 796385)),
        ),
        migrations.CreateModel(
            name='exportHeaderFields',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spdxVersion', models.CharField(max_length=100)),
                ('dataLicense', models.CharField(max_length=100)),
                ('spdxId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('documentNamespace', models.CharField(max_length=100)),
                ('creationInfoComment', models.TextField()),
                ('creationInfoCreated', models.DateTimeField(default=datetime.datetime(2022, 8, 17, 21, 16, 22, 796385))),
                ('creationInfoCreatorsTools', models.CharField(blank=True, max_length=100, null=True)),
                ('creationInfoCreatorsOrganization', models.CharField(blank=True, max_length=100, null=True)),
                ('creationInfoCreatorsPerson', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField()),
                ('setHeader', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
