from django.db import models

from core.models import TimeStampModel

class Stay(TimeStampModel):
    name           = models.CharField(max_length=45)
    address        = models.CharField(max_length=200)
    latitude       = models.DecimalField(max_digits=20, decimal_places=10)
    longitude      = models.DecimalField(max_digits=20, decimal_places=10)
    keyword        = models.CharField(max_length=45)
    summary        = models.CharField(max_length=200)
    content_top    = models.TextField(max_length=200)
    content_bottom = models.TextField(max_length=200)
    phone_number   = models.CharField(max_length=200)
    email          = models.CharField(max_length=200)
    stay_type      = models.ForeignKey('StayType', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'stays'

class Theme(models.Model):
    name   = models.CharField(max_length=45)
    icon   = models.CharField(max_length=45)
    detail = models.CharField(max_length=200)
    stay   = models.ManyToManyField('Stay', related_name='themes')

    class Meta:
        db_table = 'themes'

class StayType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'stay_type'

class Room(TimeStampModel):
    name         = models.CharField(max_length=45)
    content      = models.CharField(max_length=400)
    max_capacity = models.IntegerField()
    min_capacity = models.IntegerField()
    checkout     = models.CharField(max_length=45)
    checkin      = models.CharField(max_length=45)
    area         = models.DecimalField(max_digits=15, decimal_places=2)
    bed          = models.CharField(max_length=45)
    stay         = models.ForeignKey('Stay', on_delete=models.CASCADE)
    room_type    = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'rooms'

class RoomType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'room_type'

class Feature(models.Model):
    name = models.CharField(max_length=45)
    icon = models.CharField(max_length=200)
    room = models.ManyToManyField('Room', related_name='features')

    class Meta:
        db_table = 'features'

class Amenity(models.Model):
    name = models.CharField(max_length=45)
    room = models.ManyToManyField('Room', related_name='amenities')

    class Meta:
        db_table = 'amenities'

class AddOn(models.Model):
    name = models.CharField(max_length=45)
    room = models.ManyToManyField('Room', related_name='add_ons')

    class Meta:
        db_table = 'add_ons'

class RoomOption(models.Model):
    price  = models.DecimalField(max_digits=15, decimal_places=2)
    room   = models.ForeignKey('Room', on_delete=models.CASCADE)
    option = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_options'

class Option(models.Model):
    season = models.CharField(max_length=45)

    class Meta:
        db_table = 'options'

class StayImage(models.Model):
    image = models.CharField(max_length=400)
    stay  = models.ForeignKey('Stay', on_delete=models.CASCADE)

    class Meta:
        db_table = 'stay_images'

class RoomImage(models.Model):
    image = models.CharField(max_length=400)
    room  = models.ForeignKey('Room', on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_images'
