# Generated by Django 2.2.7 on 2019-11-17 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='email',
            field=models.CharField(default='default@example.com', max_length=200),
            preserve_default=False,
        ),
    ]
