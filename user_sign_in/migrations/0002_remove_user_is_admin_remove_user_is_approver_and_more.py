# Generated by Django 4.0.5 on 2022-06-16 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_sign_in', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_approver',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_uploader',
        ),
    ]
