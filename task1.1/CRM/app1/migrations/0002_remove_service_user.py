# Generated by Django 3.2.20 on 2023-09-03 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='user',
        ),
    ]
