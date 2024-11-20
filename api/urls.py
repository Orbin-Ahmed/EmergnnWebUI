from django.urls import path
from . import views

urlpatterns = [
    path('interaction/', views.drug_drug_interaction, name= 'interaction'),
]