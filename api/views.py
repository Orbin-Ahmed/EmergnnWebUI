from django.http import JsonResponse

def drug_interaction(request):
    drug1 = request.GET.get('drug1', '').strip()
    drug2 = request.GET.get('drug2', '').strip()

    interaction_types = {
        "aspirin:ibuprofen": "Potential gastrointestinal bleeding risk.",
        "acetaminophen:ibuprofen": "No significant interaction detected."
    }

    key = f"{drug1.lower()}:{drug2.lower()}"
    reverse_key = f"{drug2.lower()}:{drug1.lower()}"

    if key in interaction_types:
        interaction = interaction_types[key]
        interaction_type = "Single"
    elif reverse_key in interaction_types:
        interaction = interaction_types[reverse_key]
        interaction_type = "Single"
    else:
        interaction = "No interaction detected."
        interaction_type = "No interaction"

    response_data = {
        'interaction': interaction,
        'interaction_type': interaction_type
    }

    return JsonResponse(response_data)
