# Generated by Django 2.2 on 2019-05-12 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_auto_20190512_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='link',
            field=models.CharField(blank=True, max_length=127),
        ),
    ]
