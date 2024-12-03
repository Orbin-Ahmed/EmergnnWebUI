from django.shortcuts import render


def index(request):
    interaction = None
    if request.method == 'POST':
        drug1 = request.POST.get('drug1')
        drug2 = request.POST.get('drug2')

        # Placeholder for API and Graph Neural Network logic
        # Replace with your actual implementation
        interaction = f"Simulated interaction between {drug1} and {drug2}."

    return render(request, 'index.html', {'interaction': interaction})
