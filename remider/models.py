from django.db import models


class InfusionChanged(models.Model):
    """ model for saving last change of insufion set in database """
    date = models.DateTimeField()


class SensorChanged(models.Model):
    """ model for saving last change of CGM sensor in database """
    date = models.DateTimeField()


class LastTriggerSet(models.Model):
    """ model for avoiding triggers duplicates """

    date = models.DateField()


class TriggerTime(models.Model):
    """ model for saving waking up app time """
    time = models.TimeField()
