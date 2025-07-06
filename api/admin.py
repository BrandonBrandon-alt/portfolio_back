# api/admin.py

from django.contrib import admin
from .models import Project # <-- CORRECCIÓN: Se añade un punto antes de 'models'

# Register your models here.
admin.site.register(Project)