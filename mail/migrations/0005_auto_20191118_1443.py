# Generated by Django 2.2.7 on 2019-11-18 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_auto_20191118_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]