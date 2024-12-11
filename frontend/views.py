import requests
from django.shortcuts import render
from decouple import config
from .models import DrugDetail, DrugInteraction
from django.db.models import Q

# def index(request):
#     interaction = None
#     interaction_type = None
#     drug_details = []
#     drug1_name = None
#     drug2_name = None
#     generic_names = []

#     if request.method == 'POST':
#         drug1_name = request.POST.get('drug1').capitalize()
#         drug2_name = request.POST.get('drug2').capitalize()
#         backend_url = config('backend_url')
#         interaction_api_url = backend_url + 'drug-interaction/'
#         drug_info_url = backend_url + 'drug-info/'

#         public_api_url = 'https://drug-info-and-price-history.p.rapidapi.com/1/druginfo'
#         headers = {
#             'X-RapidAPI-Host': 'drug-info-and-price-history.p.rapidapi.com',
#             'X-RapidAPI-Key': config('RAPIDAPI_KEY')
#         }

#         # Fetch generic names and build the drug details
#         for drug in [drug1_name, drug2_name]:
#             public_api_response = requests.get(public_api_url, headers=headers, params={'drug': drug})
#             if public_api_response.status_code == 200:
#                 drug_data_list = public_api_response.json()
#                 if drug_data_list:
#                     drug_data = drug_data_list[0]
#                     generic_name = drug_data.get('generic_name', 'N/A')
#                     first_word_generic_name = generic_name.split()[0] if generic_name != 'N/A' else 'N/A'
#                     generic_names.append(first_word_generic_name)
                    
#                     active_ingredients = ", ".join(
#                         f"{ingredient['name']} ({ingredient['strength']})"
#                         for ingredient in drug_data.get('active_ingredients', [])
#                     )
#                     dosage_form = drug_data.get('dosage_form', 'N/A')
#                     product_type = drug_data.get('product_type', 'N/A')
#                     route = ", ".join(drug_data.get('route', []))

#                     drug_details.append({
#                         'name': drug,
#                         'generic_name': generic_name,
#                         'active_ingredients': active_ingredients,
#                         'dosage_form': dosage_form,
#                         'product_type': product_type,
#                         'route': route,
#                         'info': {},
#                     })

#             drug_info_response = requests.get(drug_info_url, params={'drug1': drug1_name, 'drug2': drug2_name})
#             if drug_info_response.status_code == 200:
#                 drug_info_details = drug_info_response.json()
            
#             # Safely update drug details with info
#             for idx, drug_key in enumerate(['drug1', 'drug2']):
#                 if idx < len(drug_details) and drug_key in drug_info_details:
#                     drug_details[idx]['info'] = drug_info_details[drug_key]['info']
                    
#         # Get Interaction Details 
#         # if len(generic_names) == 2:
#         #     interaction_response = requests.get(
#         #         interaction_api_url, 
#         #         params={'drug1': generic_names[0], 'drug2': generic_names[1]}
#         #     )
#         #     if interaction_response.status_code == 200:
#         #         interaction_data = interaction_response.json()
#         #         interaction = interaction_data.get('interaction')
#         #         interaction_type = interaction_data.get('interaction_type')
                
#         interaction = "Yes"
#         interaction_type = ["Interaction 1", "Interaction 4", "Interaction 3", "Interaction 2"]

#     return render(request, 'index.html', {
#         'interaction': interaction,
#         'interaction_type': interaction_type,
#         'drug_details': drug_details,
#     })

def index(request):
    interaction = None
    interaction_type = None
    drug_details = []
    drug1_name = None
    drug2_name = None
    generic_names = []

    if request.method == 'POST':
        drug1_name = request.POST.get('drug1').capitalize()
        drug2_name = request.POST.get('drug2').capitalize()

        backend_url = config('backend_url')
        interaction_api_url = backend_url + 'drug-interaction/'
        drug_info_url = backend_url + 'drug-info/'

        public_api_url = 'https://drug-info-and-price-history.p.rapidapi.com/1/druginfo'
        headers = {
            'X-RapidAPI-Host': 'drug-info-and-price-history.p.rapidapi.com',
            'X-RapidAPI-Key': config('RAPIDAPI_KEY')
        }
        # Get Drug Details 
        def get_or_create_drug_detail(drug_name):
            # Fetching Data From DB
            detail_obj = DrugDetail.objects.filter(name=drug_name).first()
            if detail_obj:
                print("Drug Details Fetching From DB")
                return detail_obj

            # Fetching Data From Public API
            public_api_response = requests.get(public_api_url, headers=headers, params={'drug': drug_name})
            if public_api_response.status_code == 200:
                print("Drug Details Fetching From API")
                drug_data_list = public_api_response.json()
                if drug_data_list:
                    drug_data = drug_data_list[0]
                    generic_name = drug_data.get('generic_name', 'N/A')
                    active_ingredients = ", ".join(
                        f"{ingredient['name']} ({ingredient['strength']})"
                        for ingredient in drug_data.get('active_ingredients', [])
                    )
                    dosage_form = drug_data.get('dosage_form', 'N/A')
                    product_type = drug_data.get('product_type', 'N/A')
                    route = ", ".join(drug_data.get('route', []))

                    # Save In DB
                    detail_obj = DrugDetail.objects.create(
                        name=drug_name,
                        generic_name=generic_name,
                        active_ingredients=active_ingredients,
                        dosage_form=dosage_form,
                        product_type=product_type,
                        route=route,
                        info={}
                    )
                    return detail_obj
            return None
        
        drug1_detail = get_or_create_drug_detail(drug1_name)
        drug2_detail = get_or_create_drug_detail(drug2_name)

        if drug1_detail and drug2_detail:
            generic_names.append(drug1_detail.generic_name.split()[0] if drug1_detail.generic_name and drug1_detail.generic_name != 'N/A' else 'N/A')
            generic_names.append(drug2_detail.generic_name.split()[0] if drug2_detail.generic_name and drug2_detail.generic_name != 'N/A' else 'N/A')

            # Fetching Data From Scrapper & Saving Data To DB
            drug_info_response = requests.get(drug_info_url, params={'drug1': drug1_name, 'drug2': drug2_name})
            if drug_info_response.status_code == 200:
                drug_info_details = drug_info_response.json()
                if 'drug1' in drug_info_details and 'info' in drug_info_details['drug1']:
                    drug1_detail.info = drug_info_details['drug1']['info']
                    drug1_detail.save()
                if 'drug2' in drug_info_details and 'info' in drug_info_details['drug2']:
                    drug2_detail.info = drug_info_details['drug2']['info']
                    drug2_detail.save()

            drug_details = [
                {
                    'name': drug1_detail.name,
                    'generic_name': drug1_detail.generic_name,
                    'active_ingredients': drug1_detail.active_ingredients,
                    'dosage_form': drug1_detail.dosage_form,
                    'product_type': drug1_detail.product_type,
                    'route': drug1_detail.route,
                    'info': drug1_detail.info or {},
                },
                {
                    'name': drug2_detail.name,
                    'generic_name': drug2_detail.generic_name,
                    'active_ingredients': drug2_detail.active_ingredients,
                    'dosage_form': drug2_detail.dosage_form,
                    'product_type': drug2_detail.product_type,
                    'route': drug2_detail.route,
                    'info': drug2_detail.info or {},
                }
            ]

            # Fetching Data From DB
            interaction_obj = DrugInteraction.objects.filter(
                drug1_name=generic_names[0],
                drug2_name=generic_names[1]
            ).first()

            if not interaction_obj:
                print("Interaction Fetching From API")
                # interaction = "Yes"
                # interaction_type = ["Interaction 1", "Interaction 4", "Interaction 3", "Interaction 2"]
                # Fetching Data From API
                interaction_response = requests.get(
                    interaction_api_url, 
                    params={'drug1': generic_names[0], 'drug2': generic_names[1]}
                )
                if interaction_response.status_code == 200:
                    interaction_data = interaction_response.json()
                    interaction = interaction_data.get('interaction')
                    interaction_type = interaction_data.get('interaction_type')

                    # Save To DB
                    interaction_obj = DrugInteraction.objects.create(
                        drug1_name=generic_names[0],
                        drug2_name=generic_names[1],
                        interaction=interaction,
                        interaction_types=interaction_type
                    )
            else:
                # Found In DB
                print("Interaction Fetching From DB")
                interaction = interaction_obj.interaction
                interaction_type = interaction_obj.interaction_types


    return render(request, 'index.html', {
        'interaction': interaction,
        'interaction_type': interaction_type,
        'drug_details': drug_details,
    })
