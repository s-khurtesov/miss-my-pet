# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    login = models.CharField(max_length=100, unique=True, primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    profile_photo = models.CharField(max_length=256, null=True, blank=True)


AN_SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

AN_TYPE_CHOICES = [
    ('L', 'Lost'),
    ('F', 'Found'),
]

AN_TAIL_CHOICES = [
    ('Y', 'Yes'),
    ('N', 'No'),
]


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=AN_TYPE_CHOICES)
    sex = models.CharField(max_length=1, choices=AN_SEX_CHOICES)
    photo_id = models.CharField(max_length=256, null=True, blank=True)
    paws_number = models.IntegerField()
    ears_number = models.IntegerField()
    has_tail = models.CharField(max_length=1, choices=AN_TAIL_CHOICES)
    description = models.CharField(max_length=1000, null=True, blank=True)
    last_seen_timestamp = models.DateTimeField()
    last_seen_point_lat = models.FloatField()
    last_seen_point_lng = models.FloatField()
    user_login = models.ForeignKey(User, on_delete=models.DO_NOTHING)


# https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
# https://stackoverflow.com/questions/53475999/can-one-table-has-more-than-one-primary-key-in-django
class UserFollowedAnn(models.Model):
    id = models.AutoField(primary_key=True)

    user_login = models.ForeignKey(User, on_delete=models.CASCADE)
    id_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_login', 'id_announcement'),)


class Track(models.Model):
    id = models.AutoField(primary_key=True)

    timestamp = models.DateTimeField()
    user_login = models.ForeignKey(User, on_delete=models.CASCADE)


class Point(models.Model):
    id = models.AutoField(primary_key=True)

    latitude = models.FloatField()
    longitude = models.FloatField()
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE)
    order_in_track = models.IntegerField()

    class Meta:
        unique_together = (('track_id', 'order_in_track'),)
