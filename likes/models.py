from django.db import models

from core.models  import TimeStampModel
from users.models import User
from stays.models import RoomOption

class Like(TimeStampModel):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    room_option = models.ForeignKey(RoomOption, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'