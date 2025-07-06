# api/serializers.py

from rest_framework import serializers
from models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' # Esto incluye todos los campos del modelo