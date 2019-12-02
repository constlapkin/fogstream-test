# Generated by Django 2.2.7 on 2019-11-18 04:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0003_remove_mail_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='author',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mail',
            name='status',
            field=models.BooleanField(default='True'),
            preserve_default=False,
        ),
    ]
