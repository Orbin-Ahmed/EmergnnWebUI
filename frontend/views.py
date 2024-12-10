import requests
from django.shortcuts import render
from decouple import config

def index(request):
    interaction = None
    interaction_type = None
    drug_details = []
    drug_info_details = {}
    drug1_name = None
    drug2_name = None
    generic_names = []

    if request.method == 'POST':
        drug1_name = request.POST.get('drug1')
        drug2_name = request.POST.get('drug2')
        interaction_api_url = 'http://127.0.0.1:8000/api/drug-interaction/'
        drug_info_url = 'http://127.0.0.1:8000/api/drug-info/'

        public_api_url = 'https://drug-info-and-price-history.p.rapidapi.com/1/druginfo'
        headers = {
            'X-RapidAPI-Host': 'drug-info-and-price-history.p.rapidapi.com',
            'X-RapidAPI-Key': config('RAPIDAPI_KEY')
        }

        for drug in [drug1_name, drug2_name]:
            public_api_response = requests.get(public_api_url, headers=headers, params={'drug': drug})
            if public_api_response.status_code == 200:
                drug_data_list = public_api_response.json()
                if drug_data_list:
                    drug_data = drug_data_list[0]
                    generic_name = drug_data.get('generic_name', 'N/A')
                    first_word_generic_name = generic_name.split()[0] if generic_name != 'N/A' else 'N/A'
                    generic_names.append(first_word_generic_name)
                    
                    active_ingredients = ", ".join(
                        f"{ingredient['name']} ({ingredient['strength']})"
                        for ingredient in drug_data.get('active_ingredients', [])
                    )
                    dosage_form = drug_data.get('dosage_form', 'N/A')
                    product_type = drug_data.get('product_type', 'N/A')
                    route = ", ".join(drug_data.get('route', []))

                    drug_details.append({
                        'user_name': drug,
                        'generic_name': generic_name,
                        'active_ingredients': active_ingredients,
                        'dosage_form': dosage_form,
                        'product_type': product_type,
                        'route': route
                    })

        drug_info_response = requests.get(
            drug_info_url, 
            params={'drug1': drug1_name, 'drug2': drug2_name}
        )
        
        if drug_info_response.status_code == 200:
            drug_info_details = drug_info_response.json()
        
        if len(generic_names) == 2:
            interaction_response = requests.get(
                interaction_api_url, 
                params={'drug1': generic_names[0], 'drug2': generic_names[1]}
            )
            if interaction_response.status_code == 200:
                interaction_data = interaction_response.json()
                interaction = interaction_data.get('interaction')
                interaction_type = interaction_data.get('interaction_type')

    return render(request, 'index.html', {
        'interaction': interaction,
        'interaction_type': interaction_type,
        'drug_details': drug_details,
        'drug_info_details': drug_info_details,
        'drug1_name': drug1_name,
        'drug2_name': drug2_name
    })
