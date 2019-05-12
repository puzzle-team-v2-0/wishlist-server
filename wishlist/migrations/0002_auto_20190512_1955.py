# Generated by Django 2.2 on 2019-05-12 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to=settings.AUTH_USER_MODEL),
        ),
    ]