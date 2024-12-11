from django.db import models

class DrugDetail(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, null=True, blank=True)
    active_ingredients = models.TextField(null=True, blank=True)
    dosage_form = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=255, null=True, blank=True)
    route = models.TextField(null=True, blank=True)
    info = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'generic_name')
    
    def __str__(self):
        return f"{self.name} ({self.generic_name})"


class DrugInteraction(models.Model):
    drug1_name = models.CharField(max_length=255)
    drug2_name = models.CharField(max_length=255)
    interaction = models.TextField(null=True, blank=True)
    interaction_types = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('drug1_name', 'drug2_name')
    
    def __str__(self):
        return f"{self.drug1_name} - {self.drug2_name} Interaction"
