# api/urls.py

from django.urls import path
from . import views
from .views import ProjectListCreateView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('contact/', views.contact_form_submit, name='contact_form_submit'),
]