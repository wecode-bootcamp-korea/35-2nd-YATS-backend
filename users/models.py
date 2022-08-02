from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao        = models.BigIntegerField(null=True)
    korean_name  = models.CharField(max_length=45)
    email        = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=400, null=True)

    class Meta:
        db_table = 'users'