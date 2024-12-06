from django.http import JsonResponse
from api.emergnn.make_inference import make_inference

def drug_interaction(request):
    drug1 = request.GET.get('drug1', '').strip()
    drug2 = request.GET.get('drug2', '').strip()

    # Jack call you inference function here and get the interaction(yes/no) and interaction types(list of interaction)

    inference = make_inference(drug1, drug2)

    interaction= inference.get(interaction)
    interaction_type = inference.get(interaction_type)
    response_data = {
        'interaction': interaction,
        'interaction_type': interaction_type
    }

    return JsonResponse(response_data)
