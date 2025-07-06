# api/views.py

from rest_framework import generics
# CORRECCIONES AQUÍ:
from .models import Project
from .serializers import ProjectSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer