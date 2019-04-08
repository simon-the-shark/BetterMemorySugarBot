from django.contrib import admin
from .models import InfusionChanged, SensorChanged

admin.site.register(InfusionChanged)
admin.site.register(SensorChanged)