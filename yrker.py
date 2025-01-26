import requests
from bs4 import BeautifulSoup


def get_yrker_url(url: str ):
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    container = soup.find("div", class_="view-content")
    button_container = soup.find_all("div", class_="btn btn-dark")
    for button in button_container:
        links = button.find_all("a")
        for link in links:
            href = link.get('href')  # Get the href attribute
            text = link.text.strip()  # Get the text inside the tag
            yield {"link": href, "title": text}



for yrke in get_yrker_url("https://utdanning.no/utdanningsoversikt/bygg_og_anlegg"):
    print(yrke)
