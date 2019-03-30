from django.db import models

class InfusionChanged(models.Model):
    date = models.DateTimeField("date")

class SensorChanged(models.Model):
    date = models.DateTimeField("date")

class Empty(object):
    def __init__(self):
        self.days = 0
        self.seconds = 0
        self.microseconds = 0
