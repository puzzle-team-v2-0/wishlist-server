from django.conf import settings
from django.db import models


class Wish(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='wishes'
    )
    title = models.CharField(max_length=127)
    price = models.FloatField(default=0.0)
    link = models.CharField(max_length=127)
    description = models.TextField()

