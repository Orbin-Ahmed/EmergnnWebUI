import requests
from bs4 import BeautifulSoup

def scrape_drug_information(drug_name):
    results = {}
    search_url = f"https://www.drugs.com/search.php?searchterm={drug_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find(class_="ddc-search-result-link-wrap")

        if search_results:
            description = search_results.find('p').get_text(strip=False) if search_results.find('p') else None
            results['description'] = description

    side_effects_url = f"https://www.drugs.com/sfx/{drug_name.lower()}-side-effects.html"
    response = requests.get(side_effects_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        accordion_sections = soup.find_all(class_="ddc-accordion ddc-accordion-single")

        side_effects_list = []

        for section in accordion_sections:
            summary = section.find('summary')
            title = summary.find('span', class_="ddc-text-weight-medium").get_text(strip=False) if summary and summary.find('span', class_="ddc-text-weight-medium") else ""

            content_div = section.find('div', class_="ddc-accordion-content")
            if content_div:
                list_items = content_div.find_all('li')
                items = [li.get_text(strip=False) for li in list_items]
                side_effects_list.append({
                    "title": title,
                    "details": items
                })

        results['side_effects'] = side_effects_list

    return results
