from django.db import models

from core.models  import TimeStampModel
from users.models import User
from stays.models import Stay

class Like(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'