from django.http import JsonResponse

def drug_interaction(request):
    drug1 = request.GET.get('drug1', '').strip()
    drug2 = request.GET.get('drug2', '').strip()

    # Jack call you inference function here and get the interaction(yes/no) and interaction types(list of interaction)
    interaction= "No interaction"
    interaction_type = "No interaction"
    response_data = {
        'interaction': interaction,
        'interaction_type': interaction_type
    }

    return JsonResponse(response_data)
