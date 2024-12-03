from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['post'])
def drug_interaction(request):
    drug1 = request.GET.get('drug1', '')
    drug2 = request.GET.get('drug2', '')
    interaction = f"Simulated interaction between {drug1} and {drug2}."
    
    return JsonResponse({'interaction': interaction})