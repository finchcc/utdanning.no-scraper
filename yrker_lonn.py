import json

from bs4 import BeautifulSoup
import requests

class Yrke:
    def __init__(self, link: str, title: str, education_id: str = None):
        self.link = link
        self.title = title
        self.education_id = education_id
    def __str__(self):
        return f"{self.title} ({self.link})"
    def __repr__(self):
        return self.__str__()
    
list_of_yrker: list[Yrke] = []


def test():
    yrke = list_of_yrker[10]
    print(yrke)
    response = requests.get("https://utdanning.no/yrker/beskrivelse/sivilingenior")
    html_doc = response.text
    #write html_doc to a file
    with open("html_doc_lonn.html", "w", encoding="utf-8") as file:
        file.write(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    container = soup.find("div", id="lonn-block")
    if container is None:
        print(f"Container not found for {yrke.title}")
        return
    nested_container = container.find("div", id="lonn-widget")
    if nested_container is None:
        print(f"Nested container not found for {yrke.title}")
        return
    print(nested_container)
    grid_items = nested_container.find_all("div", class_="show-grid")
    print(grid_items)
    for grid_item in grid_items:
        title_div = grid_item.find("div", class_="profession-item")
        #title is inside a span
        title = title_div.find("span").text.strip()
        lonn_grid = grid_item.find("div", class_="multiple-grid")
        for lonn_item in lonn_grid:
            lonn_div = lonn_item.find("div", class_="year-salary-item")
            lonn = lonn_div.text.strip()
            print(lonn)

        print(title, lonn)



def main():
    with open('yrker.json', 'r') as file:
        data = json.load(file)

    for yrke in data:
        list_of_yrker.append(Yrke(yrke['url'], yrke['name'], yrke['education_id']))
    
    test()
if __name__ == '__main__':
    main()



""" def get_yrker_url(url: str, education_id: str = None): 
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
            yield Yrke(href, text, education_id)"""
