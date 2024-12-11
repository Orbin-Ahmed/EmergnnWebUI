from django.contrib import admin
from .models import DrugDetail, DrugInteraction


admin.site.register(DrugDetail)

admin.site.register(DrugInteraction)
