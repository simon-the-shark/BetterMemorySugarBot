from django.db import models

class InfusionChanged(models.Model):
    """ model for saving last change of insufion set in database """
    date = models.DateTimeField()


class SensorChanged(models.Model):
    """ model for saving last change of CGM sensor in database """
    date = models.DateTimeField()
