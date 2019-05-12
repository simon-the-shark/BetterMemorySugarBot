from django.contrib import admin

from .models import InfusionChanged, SensorChanged, LastTriggerSet

admin.site.register(InfusionChanged)
admin.site.register(SensorChanged)
admin.site.register(LastTriggerSet)
