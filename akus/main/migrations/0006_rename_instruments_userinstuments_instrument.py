# Generated by Django 3.2.7 on 2022-01-17 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220117_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinstuments',
            old_name='instruments',
            new_name='instrument',
        ),
    ]
