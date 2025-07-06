# api/models.py

from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=200) # Ej: "Python, Django, React"
    image_url = models.URLField(max_length=200, blank=True)
    project_url = models.URLField(max_length=200, blank=True)
    repository_url = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title