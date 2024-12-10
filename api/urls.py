from django.urls import path
from . import views

urlpatterns = [
    path('drug-interaction/', views.drug_interaction, name='api_drug_interaction'),
    path('drug-info/', views.drug_info, name='api_drug_info'),
]