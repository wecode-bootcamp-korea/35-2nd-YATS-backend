from django.db import models

from core.models  import TimeStampModel
from users.models import User
from stays.models import Room

class BookStatus(models.Model):
    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'book_statuses'

class Book(TimeStampModel):
    book_number = models.CharField(max_length=45)
    check_in    = models.DateField()
    check_out   = models.DateField()
    status      = models.ForeignKey(BookStatus, on_delete=models.CASCADE)
    room        = models.ForeignKey(Room, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books'


