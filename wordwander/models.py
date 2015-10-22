import sys
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Word(models.Model):
    word = models.CharField(max_length=64, blank=True, null=True)
    top = models.IntegerField(blank=True, null=True)

 