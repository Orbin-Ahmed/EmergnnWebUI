from django.http import JsonResponse
from api.emergnn.make_inference import make_inference
from .scrapper import scrape_drug_information

def drug_interaction(request):
    drug1 = request.GET.get('drug1', '').strip()
    drug2 = request.GET.get('drug2', '').strip()

    inference = make_inference(drug1, drug2)

    interaction= inference.get(interaction)
    interaction_type = inference.get(interaction_type)
    response_data = {
        'interaction': interaction,
        'interaction_type': interaction_type
    }

    return JsonResponse(response_data)

def drug_info(request):
    drug1 = request.GET.get('drug1', '').strip()
    drug2 = request.GET.get('drug2', '').strip()
    if not drug1 or not drug2:
        return JsonResponse({'error': 'Both drug1 and drug2 parameters are required.'}, status=400)

    try:
        drug1_info = scrape_drug_information(drug1)
        drug2_info = scrape_drug_information(drug2)
    except Exception as e:
        return JsonResponse({'error': f'Error scraping drug information: {str(e)}'}, status=500)

    response_data = {
        'drug1': {
            'name': drug1,
            'info': drug1_info
        },
        'drug2': {
            'name': drug2,
            'info': drug2_info
        }
    }

    return JsonResponse(response_data)
