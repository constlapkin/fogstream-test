# Generated by Django 2.2.7 on 2019-11-17 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_mail_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='author',
        ),
    ]