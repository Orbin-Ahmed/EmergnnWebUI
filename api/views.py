from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['post'])
def drug_drug_interaction(request):
    
    
    return Response("Test", status=200)