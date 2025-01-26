import json
import sqlite3
import time
import requests
from bs4 import BeautifulSoup


class Education:
    def __init__(self, id: str, url: str):
        self.id = id
        self.url = url


class Yrke:
    def __init__(self, link: str, title: str, education_id: str = None):
        self.link = link
        self.title = title
        self.education_id = education_id

list_of_yrker: list[Yrke] = []


def get_yrker_url(url: str, education_id: str = None):
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
            yield Yrke(href, text, education_id)



""" for yrke in get_yrker_url("https://utdanning.no/utdanningsoversikt/bygg_og_anlegg"):
    print(yrke.link, yrke.title) """


def get_all_urls_from_db(conn: sqlite3.Connection):
    """
    Get all education IDs and URLs from the database.
    Returns a list of tuples containing (id, url).
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, url FROM basic_studies')
    list_of_education = cursor.fetchall()
    list_of_edu: list[Education] = []
    for education in list_of_education:
        list_of_edu.append(Education(education[0], education[1]))
    return list_of_edu

def get_all_yrker_from_db(conn: sqlite3.Connection):
    pass


def main():
    conn = sqlite3.connect('studies.db')
    list_of_education = get_all_urls_from_db(conn)
    print("Number of education: ", len(list_of_education))
    number_of_education = 0
    for education in list_of_education:
        for yrke in get_yrker_url(education.url, education.id):
            list_of_yrker.append(yrke)
            print("added yrke: ", yrke.title)
        time.sleep(0.1)
        number_of_education += 1
        print("Number of education: ", number_of_education , "of", len(list_of_education))
    #save to a json file
    yrker_dict = [{"name": yrke.title, "url": yrke.link, "education_id": yrke.education_id} for yrke in list_of_yrker]
    with open('yrker.json', 'w', encoding='utf-8') as f:
        json.dump(yrker_dict, f, indent=4, ensure_ascii=False)
    print("Yrker saved to yrker.json")


def check():
    conn = sqlite3.connect('studies.db')
    list_of_education = get_all_urls_from_db(conn)
    print("Number of education: ", len(list_of_education))
    number_of_education = 0
    for education in list_of_education[:4]:
        for yrke in get_yrker_url(education.url, education.id):
            list_of_yrker.append(yrke)
            print("added yrke: ", yrke.title)
        time.sleep(0.2)
        number_of_education += 1
        print("Number of education: ", number_of_education , "of", len(list_of_education))
    #save to a json file
    yrker_dict = [{"name": yrke.title, "url": yrke.link, "education_id": yrke.education_id} for yrke in list_of_yrker]
    with open('yrker.json', 'w', encoding='utf-8') as f:
        json.dump(yrker_dict, f, indent=4, ensure_ascii=False)
    print("Yrker saved to yrker.json")


def check_how_many_yrker_in_json():
    with open('yrker.json', 'r', encoding='utf-8') as f:
        yrker_dict = json.load(f)
    print("Number of yrker in json: ", len(yrker_dict))
    #print the number 500-550

#check_how_many_yrker_in_json()
