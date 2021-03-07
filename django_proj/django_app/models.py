# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    email =     models.EmailField(max_length=100, unique=True, primary_key=True)
    login =     models.CharField(max_length=100, unique=True)
    password =  models.CharField(max_length=100)