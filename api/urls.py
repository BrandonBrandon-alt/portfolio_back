# api/urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('contact/', views.contact_form_submit, name='contact_form_submit'),
]