# api/urls.py

from django.urls import path
from . import views
from .views import ProjectListCreateView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('contact/', views.contact_form_submit, name='contact_form_submit'),
]