from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id     = models.BigIntegerField(null=True)
    korean_name  = models.CharField(max_length=45, null=True)
    email        = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=45, unique=True, null=True)
    password     = models.CharField(max_length=400, null=True)
    nickname     = models.CharField(max_length=45, null=True)
    
    class Meta:
        db_table = 'users'